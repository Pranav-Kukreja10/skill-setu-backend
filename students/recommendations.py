from typing import List, Dict, Any, Optional
from collections import Counter
from django.db.models import Q
from students.models import StudentProfile, JobBenchmark
from recruiters.models import JobListing

PROJECT_SUGGESTIONS = {
    # Engineering & Technology
    "docker": "Containerize a full-stack REST API with docker-compose, setting up multi-stage builds and health checks.",
    "kubernetes": "Deploy microservices onto a local Minikube cluster with ConfigMaps, Secrets, and Ingress routing.",
    "redis": "Implement high-throughput caching and pub/sub message brokers to reduce database read latencies.",
    "postgresql": "Design normalized schemas with B-Tree/GIN indexes, explain query plans, and transaction row locks.",
    "python": "Build an asynchronous API with type hints, automated pytest suites, and resilient error handlers.",
    "django": "Develop a modular enterprise application using Django REST Framework and JWT authentication.",
    "react": "Build a responsive dashboard using React, state managers, and custom hooks with dark-mode tokens.",
    "typescript": "Migrate JavaScript components to strict TypeScript interfaces with discriminated unions.",
    "nextjs": "Create an SEO-optimized web application utilizing Server Components and dynamic route handlers.",
    "tailwind": "Implement a responsive design system using utility classes, CSS variables, and layout grids.",
    "aws": "Provision cloud infrastructure using S3, Lambda, and RDS with least-privilege IAM policies.",
    "cad": "Model parametric mechanical assemblies with kinematic stress simulations in SolidWorks/Autodesk.",
    "ansys": "Perform finite element analysis (FEA) and structural load simulations on dynamic mechanical parts.",
    "sql": "Write complex analytical window functions (ROW_NUMBER, DENSE_RANK, LAG) for cohort analysis.",
    "git": "Practice feature branching, interactive rebase, and clean pull request workflows on GitHub.",

    # Accounting & Taxation & Commerce (B.Com / CA / CMA)
    "tally": "Reconcile multi-ledger bank statements, generate GST-compliant e-invoices, and prepare balance sheet trial reports in Tally Prime.",
    "excel": "Build automated financial spreadsheets with XLOOKUP, dynamic PivotTables, conditional formatting, and Monte Carlo scenario modeling.",
    "auditing": "Execute an internal audit checklist across accounts payable, receivables, and ledger vouchers to detect discrepancy risks.",
    "taxation": "Prepare complete corporate income tax calculations, TDS deductions, and advance tax schedules under current tax slabs.",
    "gst": "Prepare monthly GSTR-1 outward returns and reconcile GSTR-2B input tax credits with purchase registers.",
    "financial reporting": "Draft complete standalone balance sheets, P&L statements, and cash flow reports in compliance with GAAP/Ind AS.",
    "quickbooks": "Configure a multi-currency small business accounting chart of accounts, automated invoicing, and reconciliation.",
    "cost accounting": "Develop activity-based costing (ABC) models and break-even variance analyses across operational product lines.",

    # Finance & Investment Banking (MBA Finance / CFA)
    "financial modeling": "Construct 3-statement financial projections and discounted cash flow (DCF) models with sensitivity tables.",
    "dcf": "Perform discounted cash flow valuation with WACC cost of capital, beta adjustments, and terminal value modeling.",
    "valuation": "Value comparable public companies (EV/EBITDA, P/E) and precedent M&A transactions for an equity pitch.",
    "bloomberg": "Extract corporate yield curves, equity fundamentals, and earnings call transcripts via Bloomberg Terminal.",
    "portfolio management": "Model Markowitz efficient frontier portfolio optimization balancing risk-adjusted Sharpe ratios.",

    # Business Administration & Management (BBA / MBA / Operations / HR)
    "business analysis": "Formulate a comprehensive Business Requirement Document (BRD) and BPMN process flow for customer onboarding.",
    "market research": "Conduct primary competitor SWOT analysis, TAM/SAM/SOM market sizing, and user persona surveys for a new launch.",
    "operations management": "Map value stream workflows, identify bottleneck delays, and implement 5S / Six Sigma waste reduction strategies.",
    "supply chain": "Model an inventory optimization EOQ (Economic Order Quantity) model with safety stock reorder thresholds.",
    "talent acquisition": "Design end-to-end talent acquisition funnels, structured competency rubrics, and onboarding SLAs for key roles.",
    "human resources": "Draft an employee performance review framework (OKR/KPI tracking) and retention risk mitigation roadmap.",
    "crm": "Configure sales pipeline stages, automated lead scoring rules, and cohort conversion dashboards in CRM.",
    "salesforce": "Build customized Salesforce opportunity pipelines, workflow automation rules, and executive forecasting reports.",
    "project management": "Construct a complete Agile project roadmap with Gantt work-breakdown structures, sprint backlogs, and risk registers.",

    # Design & Creative Arts (UI/UX, Product Design, Graphic Design)
    "figma": "Design a complete responsive mobile app design system in Figma with auto-layout, interactive prototypes, and accessible WCAG contrast.",
    "ui/ux": "Conduct user interviews, map customer journey blueprints, wireframe low-fidelity flows, and perform usability testing.",
    "ui design": "Design responsive high-fidelity UI screens featuring tokenized design systems, typography hierarchies, and dark-mode styles.",
    "ux design": "Map user pain points, build interactive wireframes, and design frictionless checkout/onboarding checkout journeys.",
    "design systems": "Build modular component libraries with tokenized typography, spacing grids, and state variants for cross-platform handoff.",
    "photoshop": "Create branded visual assets, photo manipulation compositions, and digital marketing banners with non-destructive layers.",
    "illustrator": "Design scalable brand vector identity kits, iconography guidelines, and typography packaging assets.",

    # Marketing & Growth
    "seo": "Conduct technical on-page SEO audits, keyword gap analysis, and implement structured schema markup.",
    "digital marketing": "Develop a multi-channel performance marketing campaign with CAC, ROAS projections, and A/B split testing.",
    "content strategy": "Build a topical editorial calendar, conversion copy funnels, and organic lead nurture email sequences."
}

def compute_personalized_recommendations(
    student_profile: StudentProfile,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Reverse Matching & Personalized Recommendations:
    Dynamically scores all published job & internship postings against the candidate's verified skills_matrix.
    Returns listings ranked descending by direct match percentage, with matched and missing skill breakdowns.
    """
    from django.utils import timezone
    published_listings = JobListing.objects.filter(
        status=JobListing.ListingStatus.PUBLISHED
    ).filter(
        Q(application_deadline__gte=timezone.now()) | Q(application_deadline__isnull=True)
    ).select_related('company', 'recruiter__user')

    c_matrix = student_profile.skills_matrix or {}
    c_skills = {k.lower().strip() for k in c_matrix.keys()}
    target_roles = [tr.lower().strip() for tr in (student_profile.target_roles or [])]

    scored = []
    for listing in published_listings:
        req_skills = listing.required_skills or []
        if not req_skills:
            continue

        matched = [s for s in req_skills if s.lower().strip() in c_skills]
        missing = [s for s in req_skills if s.lower().strip() not in c_skills]

        # Overlap ratio
        overlap_ratio = len(matched) / max(1, len(req_skills))

        # Target role bonus (+5% if listing title matches candidate's target job role)
        role_bonus = 5.0 if any(tr in listing.title.lower() for tr in target_roles) else 0.0

        # Verified credential bonus (+5% if student verified knowledge via AI test)
        verif_bonus = 5.0 if student_profile.is_verified else 0.0

        # Direct match percentage (0 - 100%)
        match_pct = round(min(100.0, (overlap_ratio * 90.0) + role_bonus + verif_bonus), 1)

        if match_pct >= 75.0:
            fit_level = "High Match"
        elif match_pct >= 50.0:
            fit_level = "Moderate Match"
        else:
            fit_level = "Developing Match"

        comp = listing.company
        scored.append({
            "listing_id": listing.id,
            "title": listing.title,
            "company_name": comp.name if comp else "Partner Company",
            "company_logo": comp.branding_logo_url if comp else "",
            "location": listing.location,
            "is_remote": listing.is_remote,
            "role_type": listing.role_type,
            "stipend_or_ctc": listing.stipend_or_ctc,
            "tenure": listing.tenure or "",
            "application_deadline": listing.application_deadline,
            "match_percentage": match_pct,
            "fit_level": fit_level,
            "matched_skills": matched,
            "missing_skills": missing,
            "required_skills": req_skills,
            "description": listing.description[:300] + "..." if len(listing.description) > 300 else listing.description
        })

    # Sort descending by match percentage
    scored.sort(key=lambda x: x["match_percentage"], reverse=True)

    return {
        "candidate_id": student_profile.id,
        "candidate_skills_count": len(c_skills),
        "total_recommendations": len(scored),
        "recommendations": scored[:limit]
    }


def compute_skill_gap_roadmap(
    student_profile: StudentProfile,
    target_role: Optional[str] = None
) -> Dict[str, Any]:
    """
    Skill-Gap & Upskilling Roadmap:
    Analyzes market demand across industry postings compared to candidate's verified skills.
    Produces actionable 'Skills to build next' with estimated match score gain (+X% boost)
    and practical project suggestions.
    """
    listings_qs = JobListing.objects.filter(status=JobListing.ListingStatus.PUBLISHED)
    if target_role and target_role.strip():
        role_filter = target_role.strip().lower()
        matching_listings = list(listings_qs.filter(
            Q(title__icontains=role_filter) | Q(search_corpus__icontains=role_filter)
        ))
        if matching_listings:
            listings = matching_listings
        else:
            listings = list(listings_qs)
    else:
        listings = list(listings_qs)

    c_matrix = student_profile.skills_matrix or {}
    c_skills_lower = {k.lower().strip(): v.get("weight", 0) if isinstance(v, dict) else int(v) for k, v in c_matrix.items()}

    # Aggregate skill demand across open postings
    skill_counts = Counter()
    for l in listings:
        for s in (l.required_skills or []):
            skill_counts[s.lower().strip()] += 1

    # Also augment with benchmarks if postings are few
    if len(listings) < 3:
        for bm in JobBenchmark.objects.all():
            for s in (bm.core_skills + bm.tooling_skills + bm.methodology_skills):
                skill_counts[s.lower().strip()] += 1

    total_sources = max(1, len(listings) if len(listings) >= 3 else (len(listings) + JobBenchmark.objects.count()))

    market_demand = []
    missing_skills_pool = []

    for skill, count in skill_counts.most_common(20):
        demand_pct = round((count / total_sources) * 100.0, 1)
        user_weight = c_skills_lower.get(skill, 0)
        has_skill = skill in c_skills_lower and user_weight >= 60

        item = {
            "skill": skill.capitalize(),
            "market_demand_percentage": min(100.0, demand_pct),
            "candidate_proficiency": user_weight,
            "status": "PROFICIENT" if has_skill else ("NEEDS_IMPROVEMENT" if skill in c_skills_lower else "MISSING")
        }
        market_demand.append(item)

        if not has_skill:
            missing_skills_pool.append((skill, demand_pct))

    # Formulate prioritized 'Skills to build next'
    skills_to_build = []
    for skill, demand_pct in missing_skills_pool[:6]:
        # Estimated match boost is proportional to market demand
        boost_estimate = f"+{int(min(35, max(12, demand_pct * 0.45)))}% Match Increase"
        priority = "HIGH" if demand_pct >= 50.0 else ("MEDIUM" if demand_pct >= 30.0 else "RECOMMENDED")
        
        project_idea = PROJECT_SUGGESTIONS.get(
            skill.lower(),
            f"Build a practical case study or portfolio deliverable demonstrating applied proficiency in {skill.capitalize()} with measurable business outcomes."
        )

        skills_to_build.append({
            "skill": skill.capitalize(),
            "priority": priority,
            "market_demand_percentage": demand_pct,
            "expected_match_boost": boost_estimate,
            "actionable_project": project_idea
        })

    return {
        "candidate_id": student_profile.id,
        "target_role_analyzed": target_role or "All Industry Domains",
        "total_jobs_analyzed": len(listings),
        "candidate_verified_skills_count": len(c_skills_lower),
        "market_demand_breakdown": market_demand,
        "skills_to_build_next": skills_to_build
    }
