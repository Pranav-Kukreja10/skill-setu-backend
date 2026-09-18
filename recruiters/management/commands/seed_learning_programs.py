from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from students.models import IndustrySector
from recruiters.models import Company, LearningProgram

class Command(BaseCommand):
    help = "Seed multi-domain industry learning programs across Engineering, Commerce, Management, and Design"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[-] Seeding multi-domain industry learning programs..."))

        it_sector, _ = IndustrySector.objects.get_or_create(
            name="Information Technology",
            defaults={"description": "Software, Cloud, and AI"}
        )
        mech_sector, _ = IndustrySector.objects.get_or_create(
            name="Mechanical Engineering",
            defaults={"description": "Automotive, Robotics, and Manufacturing"}
        )
        fin_sector, _ = IndustrySector.objects.get_or_create(
            name="Finance & Banking",
            defaults={"description": "FinTech, Trading, and Investment Banking"}
        )
        commerce_sector, _ = IndustrySector.objects.get_or_create(
            name="Commerce & Accounting",
            defaults={"description": "Taxation, Auditing, and Corporate Finance"}
        )
        mgmt_sector, _ = IndustrySector.objects.get_or_create(
            name="Business & Management",
            defaults={"description": "Consulting, Operations, and Business Analysis"}
        )
        design_sector, _ = IndustrySector.objects.get_or_create(
            name="Design & Creative Arts",
            defaults={"description": "UI/UX, Design Systems, and Product Design"}
        )

        companies_data = [
            {
                "name": "Google India",
                "registration_number": "CIN-U72900KA2003PTC033028",
                "is_verified": True,
                "website": "https://careers.google.com",
                "industry": it_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
                "description": "Global leader in search, cloud computing, artificial intelligence, and hyperscale systems.",
                "headquarters": "Bengaluru, Karnataka, India"
            },
            {
                "name": "Microsoft India",
                "registration_number": "CIN-U72200DL1990PTC041040",
                "is_verified": True,
                "website": "https://careers.microsoft.com",
                "industry": it_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg",
                "description": "Worldwide leader in software, cloud infrastructure, AI models, and enterprise platforms.",
                "headquarters": "Hyderabad, Telangana, India"
            },
            {
                "name": "Zerodha Broking",
                "registration_number": "CIN-U65990KA2018PTC116578",
                "is_verified": True,
                "website": "https://zerodha.com",
                "industry": fin_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/9/95/Zerodha_logo.svg/320px-Zerodha_logo.svg.png",
                "description": "India's largest retail stock broker and FinTech innovator pioneering low-latency trading infrastructure.",
                "headquarters": "Bengaluru, Karnataka, India"
            },
            {
                "name": "Morgan Stanley",
                "registration_number": "CIN-U67120MH1993FTC072704",
                "is_verified": True,
                "website": "https://www.morganstanley.com/careers",
                "industry": fin_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/3/34/Morgan_Stanley_Logo_1.svg",
                "description": "Multinational investment bank and financial services firm leading quantitative trading and risk analytics.",
                "headquarters": "Mumbai, Maharashtra, India"
            },
            {
                "name": "Deloitte India",
                "registration_number": "CIN-U74140MH1999PTC121234",
                "is_verified": True,
                "website": "https://www2.deloitte.com/in",
                "industry": commerce_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/5/56/Deloitte.svg",
                "description": "Global leader in audit, consulting, financial advisory, risk management, and tax services.",
                "headquarters": "Mumbai, Maharashtra, India"
            },
            {
                "name": "Adobe India",
                "registration_number": "CIN-U72200DL1997PTC085678",
                "is_verified": True,
                "website": "https://www.adobe.com/in",
                "industry": design_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/5/51/Adobe_Inc._logo.svg",
                "description": "Pioneering creative design software, digital experiences, Figma design tools, and document workflows.",
                "headquarters": "Noida, Uttar Pradesh, India"
            },
            {
                "name": "McKinsey & Company",
                "registration_number": "CIN-U74140DL1994FTC058912",
                "is_verified": True,
                "website": "https://www.mckinsey.com",
                "industry": mgmt_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b3/McKinsey_%26_Company_logo.svg",
                "description": "Global management consulting firm serving leading businesses, governments, and non-governmental organizations.",
                "headquarters": "Gurugram, Haryana, India"
            },
            {
                "name": "Tata Motors",
                "registration_number": "CIN-L28920MH1945PLC004520",
                "is_verified": True,
                "website": "https://www.tatamotors.com",
                "industry": mech_sector,
                "branding_logo_url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Tata_logo.svg",
                "description": "Pioneering commercial and electric vehicle engineering, battery management, and CAD simulation.",
                "headquarters": "Mumbai, Maharashtra, India"
            }
        ]

        companies = {}
        for cdata in companies_data:
            comp, _ = Company.objects.update_or_create(
                name=cdata["name"],
                defaults=cdata
            )
            companies[comp.name] = comp
            self.stdout.write(f"  [Company] {comp.name}")

        now = timezone.now()
        programs_data = [
            {
                "company": companies["Google India"],
                "title": "Google Cloud Architecture & Kubernetes Production Systems",
                "program_type": LearningProgram.ProgramType.TRAINING_PROGRAM,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Master cloud-native deployments, Kubernetes pod scheduling, multi-stage Docker builds, ingress controllers, and zero-trust microservice security.\n\nModules:\n1. Cloud Architecture Fundamentals & Microservice Primitives\n2. Containerization with Docker & Multi-Stage Builds\n3. Kubernetes Pods, Deployments & Service Discovery\n4. Distributed Observability, Prometheus Tracing & Helm Charts\n5. Zero-Trust Security & Production Hardening\n6. Capstone: Deploying High-Availability Microservices on GCP",
                "skills_covered": ["Cloud Architecture", "Kubernetes", "Docker", "GCP", "Microservices", "System Design"],
                "instructor_or_mentor": "Sundeep Rao, Principal Google Cloud Architect",
                "duration": "6 Weeks (40 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=20),
                "start_date": now + timedelta(days=25),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Microsoft India"],
                "title": "Full-Stack Enterprise Architecture with Next.js, Python & Docker",
                "program_type": LearningProgram.ProgramType.CERTIFICATION_COURSE,
                "target_audience": LearningProgram.TargetAudience.STUDENT,
                "description": "Build production-grade full-stack applications with React, Next.js Server Components, Django REST APIs, PostgreSQL transaction locking, and Docker.\n\nModules:\n1. Modern React & Next.js App Router Architecture\n2. Asynchronous Python Backend APIs & Django ORM\n3. PostgreSQL Schema Normalization & Query Tuning\n4. Docker Containerization & Local Dev Environments\n5. Authentication, JWT & ACID Transaction Isolation\n6. Capstone: Real-time Collaborative SaaS Application",
                "skills_covered": ["React", "Next.js", "Python", "Docker", "PostgreSQL", "REST APIs"],
                "instructor_or_mentor": "Dr. Rohit Saxena, Lead Architect at Microsoft",
                "duration": "8 Weeks (48 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=15),
                "start_date": now + timedelta(days=20),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Microsoft India"],
                "title": "Azure AI & Enterprise LLM Engineering Track",
                "program_type": LearningProgram.ProgramType.CERTIFICATION_COURSE,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "End-to-end certification track on building retrieval-augmented generation (RAG) pipelines, fine-tuning PyTorch models, and vector database search.\n\nModules:\n1. PyTorch Deep Learning Foundations\n2. Embedding Models & Dense Vector Retrieval\n3. Retrieval-Augmented Generation (RAG) Architecture\n4. Fine-Tuning Open-Weights Models with LoRA\n5. Multi-Agent Workflows & Tool Calling\n6. Capstone: Enterprise Knowledge Search Engine",
                "skills_covered": ["Generative AI", "Python", "PyTorch", "Vector Databases", "Prompt Engineering"],
                "instructor_or_mentor": "Dr. Meenakshi Sundaram, Partner AI Scientist, Microsoft",
                "duration": "4 Weeks (30 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=30),
                "start_date": now + timedelta(days=35),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Zerodha Broking"],
                "title": "High-Concurrency Distributed Systems & Go Backend Engineering",
                "program_type": LearningProgram.ProgramType.WORKSHOP,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Learn low-latency architecture, goroutine concurrency primitives, Redis pub/sub caching, and PostgreSQL transaction pipelines for high-throughput FinTech.\n\nModules:\n1. Go Concurrency Primitives & Memory Management\n2. Microservice IPC via gRPC & Protocol Buffers\n3. In-Memory Caching Strategies with Redis\n4. Kafka Event Streams & Message Partitioning\n5. Database Sharding & Read-Replicas\n6. Capstone: Real-Time Order Matching Engine",
                "skills_covered": ["Go", "Redis", "Kafka", "PostgreSQL", "Docker", "Algorithms"],
                "instructor_or_mentor": "Kailash Nadh, CTO Zerodha",
                "duration": "5 Weeks (32 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=18),
                "start_date": now + timedelta(days=22),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Deloitte India"],
                "title": "Advanced GST Compliance, E-Invoicing & Statutory Auditing with Tally Prime",
                "program_type": LearningProgram.ProgramType.CERTIFICATION_COURSE,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Comprehensive practical curriculum covering GSTR-1, GSTR-2B, input tax credits, electronic invoicing, TDS reconciliation, and statutory audit checklists in Tally Prime.\n\nModules:\n1. Indian GST Regulatory Framework & Slabs\n2. Multi-Ledger Accounting & E-Invoicing in Tally Prime\n3. GSTR-1 Outward Returns & GSTR-2B ITC Matching\n4. TDS Deduction Schedules & Advance Corporate Tax\n5. Statutory Internal Audit Checklists & Discrepancy Detection\n6. Capstone: End-to-End Enterprise Balance Sheet Audit",
                "skills_covered": ["Tally Prime", "GST Compliance", "Statutory Auditing", "TDS", "Taxation", "Excel Analytics"],
                "instructor_or_mentor": "CA Rajeshwar Iyer, Senior Tax Partner, Deloitte",
                "duration": "6 Weeks (36 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=21),
                "start_date": now + timedelta(days=26),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Morgan Stanley"],
                "title": "Corporate Financial Modeling, 3-Statement Forecasting & DCF Valuation",
                "program_type": LearningProgram.ProgramType.TRAINING_PROGRAM,
                "target_audience": LearningProgram.TargetAudience.STUDENT,
                "description": "Hands-on investment banking training to construct dynamic 3-statement financial models, WACC cost of capital calculations, and precedent M&A transaction valuation.\n\nModules:\n1. Dynamic 3-Statement Financial Linking (P&L, Balance Sheet, Cash Flow)\n2. Working Capital & Debt Amortization Modeling\n3. Discounted Cash Flow (DCF) with WACC Sensitivity Tables\n4. Public Comparable Company Analysis (Trading Comps)\n5. Precedent Transactions & LBO Fundamentals\n6. Capstone: Equity Pitch & Valuation Dossier",
                "skills_covered": ["Financial Modeling", "DCF Valuation", "Excel Analytics", "Financial Reporting", "Valuation"],
                "instructor_or_mentor": "Vikram Seth, Executive Director - Global Capital Markets",
                "duration": "6 Weeks (36 Hours)",
                "mode": LearningProgram.Mode.HYBRID,
                "registration_deadline": now + timedelta(days=14),
                "start_date": now + timedelta(days=19),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Deloitte India"],
                "title": "Corporate Tax Planning, Ind AS Financial Reporting & International Transfer Pricing",
                "program_type": LearningProgram.ProgramType.WORKSHOP,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Executive masterclass on Ind AS balance sheet disclosures, deferred tax asset computation, transfer pricing documentation, and corporate tax dispute mitigation.\n\nModules:\n1. Ind AS Financial Statements Presentation & Disclosures\n2. Deferred Tax Liabilities & Asset Computation\n3. International Transfer Pricing Methods & Arm's Length Standards\n4. Corporate Restructuring & M&A Tax Implications\n5. Audit Trail & MCA Mandatory Compliance\n6. Capstone: Multi-Jurisdiction Corporate Tax Filing Simulation",
                "skills_covered": ["Taxation", "Financial Reporting", "Statutory Auditing", "Cost Accounting", "Tally Prime"],
                "instructor_or_mentor": "Pooja Singhania, Managing Director - Tax Advisory",
                "duration": "4 Weeks (24 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=25),
                "start_date": now + timedelta(days=29),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Zerodha Broking"],
                "title": "Algorithmic Quantitative Trading & High-Frequency Systems Fellowship",
                "program_type": LearningProgram.ProgramType.MENTORSHIP,
                "target_audience": LearningProgram.TargetAudience.STUDENT,
                "description": "Selective mentorship program paired with senior quantitative analysts to develop backtesting strategies, Sharpe ratio optimization, and execution algorithms.\n\nModules:\n1. Market Microstructure, Order Books & Tick Data\n2. Quantitative Statistical Arbitrage & Momentum Strategies\n3. Vectorized Backtesting in Python with Backtrader\n4. Risk-Adjusted Return Metrics (Sharpe, Sortino, Max Drawdown)\n5. High-Frequency Order Routing & Execution Latency\n6. Capstone: Live Paper-Trading Deployment",
                "skills_covered": ["Financial Modeling", "Python", "Quantitative Analysis", "Algorithms", "SQL"],
                "instructor_or_mentor": "Kailash Nadh, CTO Zerodha",
                "duration": "8 Weeks (48 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=10),
                "start_date": now + timedelta(days=14),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["McKinsey & Company"],
                "title": "Enterprise Business Analysis: BRD Formulation & BPMN Process Engineering",
                "program_type": LearningProgram.ProgramType.CERTIFICATION_COURSE,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Master professional business analysis: translate stakeholder needs into Business Requirement Documents (BRDs), construct BPMN 2.0 process flows, and lead Agile user story mapping.\n\nModules:\n1. Business Analysis Planning & Stakeholder Engagement\n2. Elicitation Techniques & User Persona Interviews\n3. Formulating Comprehensive Business Requirement Documents (BRDs)\n4. BPMN 2.0 Process Flow Mapping & Gap Analysis\n5. User Story Decomposition & Acceptance Criteria\n6. Capstone: Digital Transformation BRD & Handoff Package",
                "skills_covered": ["Business Analysis", "BPMN Workflows", "Market Research", "Agile & Scrum", "Project Management"],
                "instructor_or_mentor": "Arjun Chawla, Senior Partner - Operations & Transformation",
                "duration": "5 Weeks (30 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=16),
                "start_date": now + timedelta(days=21),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["McKinsey & Company"],
                "title": "Agile Scrum Master & Product Delivery Excellence",
                "program_type": LearningProgram.ProgramType.TRAINING_PROGRAM,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Accredited program on driving Agile transformations, leading Sprint Retrospectives, managing velocity metrics in Jira, and facilitating cross-functional team delivery.\n\nModules:\n1. Agile Manifesto & Scrum Artifacts Deconstruction\n2. Sprint Planning, Capacity Estimation & Velocity Tracking\n3. Effective Daily Standups & Retrospective Facilitation\n4. Resolving Cross-Team Blockers & Managing Technical Debt\n5. Scaled Agile Framework (SAFe) Principles\n6. Capstone: Full Sprint Cycle Simulation in Jira",
                "skills_covered": ["Agile & Scrum", "Project Management", "Business Analysis", "Operations Management", "Leadership"],
                "instructor_or_mentor": "Sneha Nair, Global Agile Practice Lead",
                "duration": "4 Weeks (24 Hours)",
                "mode": LearningProgram.Mode.HYBRID,
                "registration_deadline": now + timedelta(days=12),
                "start_date": now + timedelta(days=17),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Tata Motors"],
                "title": "Global Supply Chain Optimization, Inventory EOQ & Lean Operations",
                "program_type": LearningProgram.ProgramType.WORKSHOP,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Hands-on operational management training covering Economic Order Quantity (EOQ), safety stock reorder thresholds, supplier SLA management, and Six Sigma waste reduction.\n\nModules:\n1. Supply Chain Network Design & Sourcing Strategy\n2. Inventory Optimization (EOQ & Dynamic Safety Stock)\n3. Demand Forecasting with Exponential Smoothing\n4. Value Stream Mapping & Lean Six Sigma Waste Elimination\n5. Procurement Contracting & Supplier SLA Monitoring\n6. Capstone: Manufacturing Supply Chain Resiliency Simulation",
                "skills_covered": ["Supply Chain", "Operations Management", "Business Analysis", "Project Management", "ERP"],
                "instructor_or_mentor": "Manoj Kulkarni, VP Global Supply Chain Operations",
                "duration": "4 Weeks (20 Hours)",
                "mode": LearningProgram.Mode.HYBRID,
                "registration_deadline": now + timedelta(days=19),
                "start_date": now + timedelta(days=24),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Microsoft India"],
                "title": "Enterprise CRM & Salesforce Sales Funnel Optimization",
                "program_type": LearningProgram.ProgramType.CERTIFICATION_COURSE,
                "target_audience": LearningProgram.TargetAudience.STUDENT,
                "description": "Configure customized CRM sales pipelines, lead scoring criteria, cohort conversion dashboards, and executive revenue forecasting models.\n\nModules:\n1. CRM Architecture & Customer Lifecycle Funnels\n2. Opportunity Pipeline Configuration & Lead Qualification\n3. Workflow Automation Rules & Triggered Email Sequences\n4. Executive Forecasting Dashboards & Cohort Churn Analytics\n5. Integrating CRM with Enterprise Marketing Stacks\n6. Capstone: End-to-End Enterprise CRM Implementation",
                "skills_covered": ["CRM Systems", "Salesforce", "Market Research", "Business Analysis", "Customer Analytics"],
                "instructor_or_mentor": "Kavita Ramachandran, Principal CRM Solutions Architect",
                "duration": "5 Weeks (30 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=22),
                "start_date": now + timedelta(days=27),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Adobe India"],
                "title": "Figma Enterprise Design Systems & Modular Token Architecture",
                "program_type": LearningProgram.ProgramType.CERTIFICATION_COURSE,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Industry design systems track: build scalable component libraries in Figma using auto-layout, tokenized variables (color, typography, spacing), component state variants, and accessible contrast.\n\nModules:\n1. Figma Component Primitives & Auto-Layout Mastery\n2. Tokenization: Semantic Color, Spacing & Typography Variables\n3. Interactive State Variants (Hover, Pressed, Disabled, Focus)\n4. Responsive Screen Grids & Breakpoint Strategies\n5. WCAG 2.1 Contrast Testing & Accessible Color Palettes\n6. Capstone: Complete Multi-Device Design System in Figma",
                "skills_covered": ["Figma", "Design Systems", "UI Design", "UI/UX Design", "Wireframing"],
                "instructor_or_mentor": "Tanvi Joshi, Principal Design Director, Adobe",
                "duration": "6 Weeks (36 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=17),
                "start_date": now + timedelta(days=21),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Adobe India"],
                "title": "End-to-End UI/UX User Research, Customer Journey Wireframing & Usability Testing",
                "program_type": LearningProgram.ProgramType.TRAINING_PROGRAM,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Master user-centric design: conduct generative user interviews, map customer journey blueprints, design frictionless wireframe flows, and run moderated usability tests.\n\nModules:\n1. User Persona Definition & Qualitative Interviewing\n2. Information Architecture & Card Sorting\n3. Low-Fidelity Wireframing & Task-Flow Mapping\n4. High-Fidelity Clickable Prototyping in Figma\n5. Moderated Usability Testing & Heuristic Evaluation\n6. Capstone: Mobile App Redesign with User Research Report",
                "skills_covered": ["UI/UX Design", "User Research", "Wireframing", "Prototyping", "Figma"],
                "instructor_or_mentor": "Dr. Prateek Merchant, Head of Experience Research, Adobe",
                "duration": "6 Weeks (36 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=14),
                "start_date": now + timedelta(days=18),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Microsoft India"],
                "title": "Inclusive Product Design & WCAG 2.1 AAA Accessibility Standards",
                "program_type": LearningProgram.ProgramType.WORKSHOP,
                "target_audience": LearningProgram.TargetAudience.ALL,
                "description": "Hands-on engineering and design workshop on building accessible interfaces: screen reader audits, keyboard navigation traps, focus indicators, and semantic HTML accessibility.\n\nModules:\n1. WCAG 2.1 Principles: Perceivable, Operable, Understandable, Robust\n2. Color Contrast Ratios, Colorblindness & Visual Ergonomics\n3. Screen Reader Testing with NVDA & VoiceOver\n4. Accessible Form Controls, ARIA Landmarks & Live Regions\n5. Automated Accessibility Audits in CI/CD\n6. Capstone: Auditing & Remediating an Inaccessible Web Application",
                "skills_covered": ["WCAG Accessibility", "UI/UX Design", "Design Systems", "Figma", "HTML5 Semantics"],
                "instructor_or_mentor": "Siddharth Menon, Accessibility Engineering Lead, Microsoft",
                "duration": "3 Weeks (18 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=24),
                "start_date": now + timedelta(days=28),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=800&q=80"
            },
            {
                "company": companies["Adobe India"],
                "title": "Interactive Micro-Interactions, Motion Design & Developer Handoff",
                "program_type": LearningProgram.ProgramType.WORKSHOP,
                "target_audience": LearningProgram.TargetAudience.STUDENT,
                "description": "Bridge design and engineering with dynamic micro-animations: spring physics, scroll-driven interactions, Lottie vector animations, and production spec handoff.\n\nModules:\n1. Motion Principles: Easing Curves, Choreography & Spatial Continuity\n2. Spring Physics & Gesture-Driven Micro-Interactions\n3. Vector Animation with After Effects & Lottie\n4. Prototyping Complex States in Figma & Principle\n5. Design Token Synchronization & Developer Handoff\n6. Capstone: Interactive Product Experience with Motion Specs",
                "skills_covered": ["Figma", "UI Design", "Interaction Design", "Prototyping", "Design Systems"],
                "instructor_or_mentor": "Meera Vohra, Lead Interaction Designer, Adobe",
                "duration": "4 Weeks (24 Hours)",
                "mode": LearningProgram.Mode.ONLINE,
                "registration_deadline": now + timedelta(days=15),
                "start_date": now + timedelta(days=20),
                "is_certified": True,
                "branding_banner_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80"
            }
        ]

        count = 0
        for pdata in programs_data:
            prog, created = LearningProgram.objects.update_or_create(
                company=pdata["company"],
                title=pdata["title"],
                defaults=pdata
            )
            count += 1
            status = "Created" if created else "Updated"
            self.stdout.write(f"  [{count}/16] [{status}] '{prog.title}' by {prog.company.name}")

        self.stdout.write(self.style.SUCCESS(f"[+] Successfully seeded {count} multi-domain learning programs!"))
