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
    "content strategy": "Build a topical editorial calendar, conversion copy funnels, and organic lead nurture email sequences.",
    "quality assurance": "Establish an automated QA testing pipeline with unit, integration, and regression suites and defect lifecycle tracking.",
    "test automation": "Architect a data-driven test automation framework in Selenium/Playwright with parallel execution and HTML reporting.",
    "functional testing": "Design a comprehensive test matrix and boundary-value test suite covering critical business journeys.",
    "api testing": "Build an automated REST API test collection in Postman/Newman with assertions on schemas, status codes, and latency.",
    "selenium": "Automate cross-browser cross-device UI flows with Selenium WebDriver and Page Object Model (POM) architecture.",
    "cypress": "Write fast, reliable end-to-end browser tests in Cypress with mocked network requests and CI workflow integration.",
    "jira": "Configure an Agile Scrum sprint board with customized issue types, workflow transitions, and bug severity SLAs.",
    "hp alm quality center": "Manage requirement traceability matrices and defect lifecycle tracking across testing sprints.",
    "hp qtp": "Build regression test automation scripts using descriptive programming and shared object repositories.",
    "performance testing": "Execute load and stress testing using JMeter or k6 to identify server bottlenecks and throughput limits.",
    "c": "Develop low-level systems utilities with pointers, dynamic memory allocation, and Valgrind leak checking.",
    "vb script": "Automate enterprise test scripts with modular error handling, regular expressions, and file I/O operations.",
    "automation": "Design an automated regression testing harness triggered on git pull requests with test artifact generation."
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

        role_bonus = 0.0
        l_title_lower = listing.title.lower().strip()
        for tr in target_roles:
            if tr in l_title_lower or l_title_lower in tr:
                role_bonus = 5.0
                break

        # Verified credential bonus (+5% if student verified knowledge via AI test)
        verif_bonus = 5.0 if student_profile.is_verified else 0.0

        # NEP 2020 Multidisciplinary Minor Synergy Check (Clause 11.3)
        is_nep_multidisciplinary_match = False
        nep_synergy_bonus = 0.0
        nep_match_reason = None
        if student_profile.minor_specialization and student_profile.minor_specialization.lower().strip() != "none":
            minor_kw = student_profile.minor_specialization.lower().strip()
            relevant_kws = {minor_kw}
            if "ai" in minor_kw or "intelligence" in minor_kw:
                relevant_kws.update(["python", "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch"])
            elif "design" in minor_kw or "ui" in minor_kw:
                relevant_kws.update(["figma", "ui/ux", "wireframing", "adobe xd", "prototyping"])
            elif "finance" in minor_kw:
                relevant_kws.update(["financial modeling", "excel", "accounting", "valuation", "taxation", "tally"])
            elif "business" in minor_kw or "management" in minor_kw:
                relevant_kws.update(["business analysis", "market research", "project management", "crm", "salesforce"])
            
            minor_matches = [s for s in req_skills if s.lower().strip() in relevant_kws]
            if minor_matches:
                is_nep_multidisciplinary_match = True
                nep_synergy_bonus = 5.0
                deg_label = student_profile.degree or "Major"
                nep_match_reason = f"NEP 2020 Multidisciplinary Synergy: Bridges your {deg_label} with your '{student_profile.minor_specialization}' Minor ({', '.join(minor_matches[:3])})!"

        # Direct match percentage (0 - 100%)
        match_pct = round(min(100.0, (overlap_ratio * 85.0) + role_bonus + verif_bonus + nep_synergy_bonus), 1)

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
            "min_nheqf_level": getattr(listing, 'min_nheqf_level', 'LEVEL_4_5') or 'LEVEL_4_5',
            "stipend_or_ctc": listing.stipend_or_ctc,
            "tenure": listing.tenure or "",
            "application_deadline": listing.application_deadline,
            "match_percentage": match_pct,
            "fit_level": fit_level,
            "is_nep_multidisciplinary_match": is_nep_multidisciplinary_match,
            "nep_match_reason": nep_match_reason,
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
    resolved_target_role = target_role.strip() if (target_role and target_role.strip()) else ""
    if not resolved_target_role:
        if student_profile.target_roles and len(student_profile.target_roles) > 0:
            resolved_target_role = student_profile.target_roles[0]
        elif student_profile.role_fit_matrix:
            sorted_fits = sorted(
                student_profile.role_fit_matrix.items(),
                key=lambda item: float(item[1].get("score", 0) if isinstance(item[1], dict) else 0),
                reverse=True
            )
            if sorted_fits:
                resolved_target_role = sorted_fits[0][0]

    c_matrix = student_profile.skills_matrix or {}
    c_skills_lower = {}
    for k, v in c_matrix.items():
        val = v.get("weight", 0) if isinstance(v, dict) else int(v)
        c_skills_lower[k.lower().strip()] = int(val)

    for cat_list in (student_profile.skills_categorized or {}).values():
        if isinstance(cat_list, list):
            for sk in cat_list:
                sk_clean = sk.lower().strip()
                if sk_clean not in c_skills_lower:
                    c_skills_lower[sk_clean] = int(student_profile.overall_confidence_score or 75)

    listings_qs = JobListing.objects.filter(status=JobListing.ListingStatus.PUBLISHED).only('id', 'title', 'search_corpus', 'required_skills')
    
    skill_counts = Counter()
    matched_listings = []
    
    if resolved_target_role:
        role_words = [w.lower() for w in resolved_target_role.split() if len(w) > 2]
        for l in listings_qs:
            title_lower = (l.title or "").lower()
            corpus_lower = (l.search_corpus or "").lower()
            if any(w in title_lower or w in corpus_lower for w in role_words):
                matched_listings.append(l)
        
        benchmarks = list(JobBenchmark.objects.filter(
            Q(role_title__icontains=resolved_target_role) |
            Q(sector__name__icontains=resolved_target_role)
        ))
        if not benchmarks:
            for w in role_words:
                bms = list(JobBenchmark.objects.filter(role_title__icontains=w))
                if bms:
                    benchmarks.extend(bms)
        
        for bm in benchmarks:
            for s in (bm.core_skills + bm.tooling_skills + bm.methodology_skills):
                skill_counts[s.lower().strip()] += 3

    if not matched_listings:
        for l in listings_qs:
            reqs = [r.lower().strip() for r in (l.required_skills or [])]
            if any(sk in c_skills_lower for sk in reqs):
                matched_listings.append(l)

    effective_listings = matched_listings if matched_listings else list(listings_qs)

    for l in effective_listings:
        for s in (l.required_skills or []):
            skill_counts[s.lower().strip()] += 1

    for sk_name in c_skills_lower.keys():
        if sk_name not in skill_counts:
            skill_counts[sk_name] += 1

    total_sources = max(1, len(effective_listings) + 2)

    market_demand = []
    missing_skills_pool = []

    priority_skills = []
    for sk, weight in c_skills_lower.items():
        if sk in skill_counts:
            priority_skills.append(sk)

    other_skills = [sk for sk, _ in skill_counts.most_common(25) if sk not in priority_skills]
    ordered_skills = priority_skills[:10] + other_skills[:10]

    seen = set()
    for skill in ordered_skills:
        if skill in seen:
            continue
        seen.add(skill)
        count = skill_counts.get(skill, 1)
        demand_pct = round(min(100.0, max(30.0, (count / total_sources) * 100.0)), 1)
        user_weight = c_skills_lower.get(skill, 0)
        has_skill = skill in c_skills_lower and user_weight >= 60

        item = {
            "skill": skill.title() if len(skill) > 3 else skill.upper(),
            "market_demand_percentage": demand_pct,
            "candidate_proficiency": user_weight,
            "status": "PROFICIENT" if has_skill else ("NEEDS_IMPROVEMENT" if skill in c_skills_lower else "MISSING")
        }
        market_demand.append(item)

        if not has_skill:
            missing_skills_pool.append((skill, demand_pct))

    missing_skills_pool.sort(key=lambda x: x[1], reverse=True)

    skills_to_build = []
    for skill, demand_pct in missing_skills_pool[:6]:
        boost_estimate = f"+{int(min(35, max(12, demand_pct * 0.45)))}% Match Increase"
        priority = "HIGH" if demand_pct >= 60.0 else ("MEDIUM" if demand_pct >= 40.0 else "RECOMMENDED")
        
        project_idea = PROJECT_SUGGESTIONS.get(
            skill.lower(),
            f"Build a practical case study or portfolio deliverable demonstrating applied proficiency in {skill.title()} with measurable outcomes."
        )

        skills_to_build.append({
            "skill": skill.title() if len(skill) > 3 else skill.upper(),
            "priority": priority,
            "market_demand_percentage": demand_pct,
            "expected_match_boost": boost_estimate,
            "actionable_project": project_idea
        })

    return {
        "candidate_id": student_profile.id,
        "target_role_analyzed": resolved_target_role or "Resume Domain Profile",
        "total_jobs_analyzed": len(effective_listings),
        "candidate_verified_skills_count": len(c_skills_lower),
        "market_demand_breakdown": market_demand,
        "skills_to_build_next": skills_to_build
    }
