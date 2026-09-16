# Skill Setu — Backend Feature Inventory & Master Tracker

This document provides a comprehensive, feature-by-feature breakdown of everything implemented inside the `skillsetu-backend` platform. It serves as an internal tracking guide for developers, a contract reference for the frontend team, and an evaluation roadmap for the Smart India Hackathon (SIH) jury.

---

## 📑 Table of Contents
1. [Architecture & System Foundation](#1-architecture--system-foundation)
2. [Identity, Authentication & Stateless RBAC](#2-identity-authentication--stateless-rbac)
3. [Universal Multi-Domain Screening & Resume Parsing](#3-universal-multi-domain-screening--resume-parsing)
4. [Adaptive Testing, Viva Grading & Anti-Cheat System](#4-adaptive-testing-viva-grading--anti-cheat-system)
5. [Digital Student Portfolio & Live Internship Tracking](#5-digital-student-portfolio--live-internship-tracking)
6. [Reverse Matching, Recommendations & Upskilling Roadmap](#6-reverse-matching-recommendations--upskilling-roadmap)
7. [Two-Way 3-Signal Hybrid NLP Search](#7-two-way-3-signal-hybrid-nlp-search)
8. [Multi-Domain Affirmative Action & Government Schemes Radar](#8-multi-domain-affirmative-action--government-schemes-radar)
9. [Candidate Profile Settings & Full Personalization](#9-candidate-profile-settings--full-personalization)
10. [Corporate Recruiter Suite & ACID Hiring Pipeline](#10-corporate-recruiter-suite--acid-hiring-pipeline)
11. [Institutional Oversight & Faculty Placement Analytics](#11-institutional-oversight--faculty-placement-analytics)
12. [Corporate Learning Programs & Hackathon Challenges](#12-corporate-learning-programs--hackathon-challenges)
13. [Faculty Industry Internships, FDPs & Research Collaborations](#13-faculty-industry-internships-fdps--research-collaborations)
14. [Scalability, Database Performance & Resilience Safeguards](#14-scalability-database-performance--resilience-safeguards)
15. [Core Mathematical & Anti-Cheat Scoring Formulas](#15-core-mathematical--anti-cheat-scoring-formulas)
16. [Complete API Endpoint Catalog](#16-complete-api-endpoint-catalog)

---

## 1. Architecture & System Foundation

- **Framework**: Django 5.2 + Django Ninja 1.7 (combines Django ORM data integrity with FastAPI's Pydantic v2 engine and OpenAPI autogeneration).
- **Asynchronous Protocol**: ASGI (`asgiref`, `anyio`) with sub-millisecond execution.
- **Database**: PostgreSQL 16+ with native `pgvector` dense vector indexing.
- **API Documentation**: Interactive OpenAPI 3.0 / Swagger UI dynamically generated at `/api/v1/docs`.
- **Modular Domain Architecture**:
  - `accounts/`: Authentication, JWT tokens, OAuth2 SSO, role guards.
  - `students/`: Parsing, fitment, testing, grading, recommendations, roadmaps, portfolios, schemes.
  - `recruiters/`: Company profiles, job lifecycle, ACID application pipeline, corporate programs.
  - `institutions/`: Colleges, departments, faculty profiles, institutional placement radar, FDPs.

---

## 2. Identity, Authentication & Stateless RBAC

### Features
- **4-Role User Model**: Custom user model supporting `STUDENT`, `RECRUITER`, `ACADEMIA`, and `ADMIN` (with full candidate/student parity).
- **Signed 24-Hour JWT Tokens**: Cryptographically signed HS256 JWTs embedding `user_id`, `username`, and `role`.
- **Stateless Role Authorization Guards**:
  - `RecruiterAuth`: Restricts endpoints strictly to `RECRUITER` and `ADMIN`.
  - `StudentAuth` (aliased to `CandidateAuth`): Restricts to `STUDENT`, `CANDIDATE`, `ADMIN`.
  - `AcademiaAuth`: Restricts to `ACADEMIA` and `ADMIN`.
  - **Zero-DB Role Check**: Pre-validates role claims directly from the decoded JWT payload *before* hitting PostgreSQL, instantly rejecting unauthorized roles with 0 database roundtrips.
- **OAuth2 Single Sign-On (Google & GitHub)**:
  - Supports Google ID Tokens and GitHub OAuth authorization codes.
  - Auto-provisions new user accounts, sets avatar URLs, and dispatches automated profile creation signals (e.g. `StudentProfile`).
  - Gracefully links existing accounts by verified email without duplicate row conflicts.
  - **Pitch-Resilient Presentation Mode**: Offline presentation tokens (`demo_google_*`, `demo_github_*`) create genuine test users and JWTs offline, guaranteeing 100% demo uptime even if venue Wi-Fi drops.

---

## 3. Universal Multi-Domain Screening & Resume Parsing

### Features
- **Zero-Disk In-Memory Parsing**:
  - Uploaded PDF/DOCX binaries are parsed entirely in-memory using `pypdf` and `python-docx` (0ms disk write delay, eliminating temp file leaks).
- **Task-Specific Cloud AI Gateway**:
  - Routes resume parsing to `gemini-3.1-flash-lite` with a 120-second resilient timeout.
  - Configurable `.env` fallback hook to local RTX 4060 GPU via Ollama (`qwen3.5:9b`).
- **Universal Multi-Domain Coverage**:
  - Full evaluation and benchmarking across:
    1. **Engineering & Technology (B.Tech, BCA, MCA)**: Python, Django, React, AWS, Docker, Microservices, CAD/FEA.
    2. **Commerce & Accounting (B.Com, M.Com, CA, CMA)**: Tally Prime, GST filing, TDS, statutory auditing, GAAP/IFRS balance sheets, QuickBooks.
    3. **Business & Management (BBA, MBA, PGDM)**: Business analysis, SWOT, market sizing, supply chain, CRM (Salesforce), BRD authoring.
    4. **Design & Creative Arts (B.Des, M.Des, UI/UX)**: Figma design systems, customer journey wireframing, WCAG accessibility, usability research.
- **Dynamic Universal 4-Tier Categorization**:
  - Automatically classifies candidate competencies across **ANY** technical or non-technical field into 4 ontological tiers:
    1. **`technical_skills` (Core Functional Knowledge)**: The domain-specific theory, subject matter, and functional competencies required to execute the job (e.g. *Financial Auditing, DCF Valuation, Machine Learning, UI Wireframing, Thermodynamics*).
    2. **`frameworks` (Methodologies, Standards & Architectures)**: Standard operating procedures, regulatory frameworks, compliance standards, and architectural blueprints (e.g. *GAAP, IFRS, Agile/Scrum, Design Thinking, GD&T, Six Sigma, React, Django*).
    3. **`tools` (Software, Platforms & Utilities)**: Applications, software suites, platforms, or physical equipment used to perform work (e.g. *Tally Prime, Salesforce CRM, Figma, SAP FICO, Excel, AutoCAD, Bloomberg Terminal, Docker*).
    4. **`soft_skills` (Human Factor & Leadership)**: Behavioral, interpersonal, and collaborative abilities (e.g. *Stakeholder Presentation, Client Negotiation, Active Listening, Conflict Resolution*).

| Domain | `technical_skills` (Core) | `frameworks` (Standards & Methodologies) | `tools` (Platforms & Software) | `soft_skills` (Human Factor) |
|---|---|---|---|---|
| **Commerce & Accounting** | Statutory Auditing, Tax Filing, Cost Accounting | **GAAP**, **IFRS**, Ind AS, GST Regulatory Rules | Tally Prime, QuickBooks, SAP FICO, MS Excel | Client Advisory, Regulatory Ethics, Precision |
| **Business & Management** | Market Sizing, DCF Valuation, Supply Chain Logistics | **SWOT**, **Porter's 5 Forces**, **Agile/Scrum**, Lean Six Sigma | Salesforce CRM, Jira, HubSpot, Tableau, PowerBI | Stakeholder Management, Strategic Negotiation |
| **Design & Creative Arts** | Heuristic Usability Research, Information Architecture | **Design Thinking**, **WCAG 2.1 Accessibility**, Atomic Design | Figma, Adobe Illustrator, Photoshop, Miro | Empathy, Storytelling, Design Critique |
| **Engineering & Technology**| Distributed Systems, Database Optimization, Algorithms | REST APIs, MVC, CI/CD, React, Django, Spring Boot | Git, GitHub, Postman, AWS Console, Docker | Team Collaboration, Technical Documentation |
| **Mechanical Engineering** | Fluid Dynamics, Thermodynamics, Machine Design | **GD&T**, **FEA (Finite Element Analysis)**, ISO 9001 | AutoCAD, SolidWorks, ANSYS, CATIA, MATLAB | Industrial Safety Compliance, Vendor Management |

- **Data Provenance**:
  - Preserves verbatim, un-normalized parsed strings in `StudentProfile.raw_extracted_skills` alongside canonical benchmark tags.
- **Uncommitted Resume Preview (`/api/v1/students/resume-preview-extract`)**:
  - Allows candidates to preview AI-extracted skills, projects, and roles without saving to the database.

---

## 4. Adaptive Testing, Viva Grading & Anti-Cheat System

### Features
- **Dynamic Adaptive Assessment Generation**:
  - Generates 5 progressive difficulty questions (MCQs + Viva architectural/practical scenarios) tailored to the candidate's target role.
- **Server-Side Answer & Rubric Withholding**:
  - Evaluation rubrics, correct answers, and scoring keys are stored in `TestSession` server-side only; Swagger payloads and frontend responses never expose answer keys.
- **Real-Time Mixed Evaluation**:
  - MCQs evaluated instantly in-memory.
  - Technical vivas evaluated via cloud AI against explicit multi-tier grading rubrics.
- **Anti-Cheat & Plagiarism Protections**:
  - **MCQ Time-Decay Multiplier ($M_t$)**: Rewards instant mastery (≤15s: 100% credit), applies linear decay between 15–60s down to 70%, and caps at 70% minimum for >60s external search hesitation.
  - **Keystroke Velocity Check**: Detects instant copy-pasting of long viva answers and logs audit flags.
  - **Capped-Root Plagiarism Penalty ($CS$)**: Compares pre-test resume claims ($R_s$) with actual demonstrated test scores ($A_s$). Suspicious gaps trigger a non-linear mathematical penalty capping unearned confidence scores.
- **Zero-Unearned-Score Retest Policy**:
  - If external AI fails or times out during viva grading, the backend **NEVER** awards unearned baseline points (cognitive score = 0, confidence score = 0).
  - The system politely takes blame on our side (*"Oops! Our neural pathways hit a brief detour on our end..."*), keeps the session open (`is_completed=False`), and mandates an immediate retest (`retest_required=True`) to maintain assessment integrity.

---

## 5. Digital Student Portfolio & Live Internship Tracking

### Features
- **Comprehensive Candidate Portfolio (`/students/portfolio/me` & `/students/{id}/portfolio`)**:
  - Aggregates verified skills matrix ($W_s$), progressive cognitive score ($A_s$), confidence score ($CS$), profile strength score ($P_{\text{overall}}$), academic CGPA/transcripts, verified industry certifications, production projects, completed internships with ratings, and hackathon achievements (SIH, IEEE).
- **Blind Screening Toggle (`?blind=true`)**:
  - Automatically redacts candidate personal identifiable information (PII):
    - Name $\to$ `"Candidate #ID"`
    - Email $\to$ `"[REDACTED]"`
    - Institution $\to$ `"[REDACTED]"`
  - Preserves verified cognitive scores, skill weights ($W_s$), and project deliverables for unbiased shortlisting.
- **Live Internship Milestone Logging (`/students/internships/{id}/log-milestone`)**:
  - Student logs weekly milestone updates (week number, summary of deliverables, hours worked, GitHub/deliverable repository URL).
  - Automatically transitions internship status to `IN_PROGRESS`.
- **Recruiter Supervision & Verified Credentialing**:
  - Recruiter logs mentor evaluation remarks, records star performance ratings (1.0 to 5.0), and attaches completion certificate URLs.
  - Setting status to `COMPLETED` automatically inserts the verified credential into the candidate's public digital portfolio and dispatches real-time alerts.

---

## 5B. NEP 2020 Real-Time Policy Engine (NCrF, APAAR, AICTE & PARAKH)

### Live Functioning Features
- **APAAR ID & Academic Bank of Credits (ABC) Integration**:
  - `StudentProfile` stores 12-digit **APAAR ID** (*"One Nation, One Student ID"*) and **ABC ID** with format validation and verification status.
- **National Credit Framework (NCrF) Real-Time Credit Calculator**:
  - Dynamically calculates academic credits earned by candidates from verified activities:
    $$\text{NCrF Credits} = \sum \left(\left\lfloor \frac{\text{internship\_weeks}}{4} \right\rfloor \times 2\right) + (\text{verified\_certifications} \times 1)$$
    - 4-week verified internship = **2 NCrF Credits**
    - 8-week verified internship = **4 NCrF Credits**
    - Verified industry credential = **1 NCrF Credit**
- **AICTE Mandatory Internship Activity Points Tracker**:
  - AICTE requires 75–100 Activity Points for undergraduate engineering degrees.
  - Automatically calculates points based on logged mentor-verified internship hours:
    $$\text{AICTE Points} = \min\left(100, \left\lfloor \frac{\text{logged\_hours}}{40} \right\rfloor \times 10\right)$$
  - Tracks completion percentage (e.g. `40 / 100 Points`) and flags when the 75-point threshold is met.
- **Multidisciplinary "Major + Minor" Skill-Bridge Matching (NEP Clause 11.3)**:
  - Tracks candidate's `minor_specialization` (e.g. Data Analytics, FinTech, UI/UX).
  - Reverse matching engine detects cross-disciplinary synergy between candidate's Major and Minor:
    - Awards **+5% Multidisciplinary Synergy Boost**.
    - Tags opportunities with dynamic badges: `⚡ NEP 2020 Multidisciplinary Synergy: Bridges your B.Com with your Data Analytics Minor!`.
- **Multiple Entry & Multiple Exit (MEME) Pathway (NHEQF Levels 4.5 to 8.0)**:
  - Supports candidates at any exit stage: `LEVEL_4_5` (UG Certificate), `LEVEL_5_0` (UG Diploma), `LEVEL_5_5` / `LEVEL_6_0` (Bachelor's), `LEVEL_7_0` (Master's).
  - Job listings specify `min_nheqf_level`, allowing certificate/diploma exit candidates to discover accessible vocational roles.
- **PARAKH 360° Holistic Competency Assessment (NEP Clause 4.35)**:
  - Formulates a 360-degree assessment across 4 domains: Cognitive (45%), Practical Application (30%), Vocational Credentials (15%), and Academic Performance (10%).
  - Outputs PARAKH grade: `Exemplary (A+)`, `Proficient (A)`, or `Developing (B)`.
- **Official DigiLocker / ABC Academic Credit Transcript Export (`GET /api/v1/students/me/nep-transcript`)**:
  - Exports a cryptographically signed (SHA256 hash) credit transcript payload ready for university examination cells and DigiLocker credit ingestion.

---

## 5C. GitHub Screening & Anti-"Vibe Coding" Engineering Radar (CSE/IT)

### Live Functioning Features
- **Zero-Permission Public Screening**:
  - Analyzes public repositories without requiring student passwords or private OAuth repository scopes.
  - Automatically extracts candidate handles from profile/resume URLs (`https://github.com/{username}`).
  - Server-side rate-limit management (5,000 req/hr with server token) and pitch-resilient presentation fallback (`demo_*`).
- **Commit Cadence & Conventional Commits Hygiene**:
  - Analyzes recent commit messages against **Conventional Commits** (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `ci:`).
  - Measures commit message quality, average length, and frequency over time to separate continuous engineering from 1-day AI prompt code dumps.
- **Production Engineering Readiness Score (0–100)**:
  - Evaluates real-world software craft across 5 objective signals:
    1. **CI/CD Workflows (+25 pts)**: Automated GitHub Actions pipelines (`.github/workflows`).
    2. **Automated Testing (+25 pts)**: Unit & integration test suites (`pytest`, `jest`, `tests/`).
    3. **Containerization (+20 pts)**: `Dockerfile`, `docker-compose.yml`.
    4. **Conventional Commits (+15 pts)**: Percentage adherence to structured commit messages.
    5. **Code Hygiene & Linters (+15 pts)**: Linter configs (`.eslintrc`, `.flake8`, `ruff.toml`) & architectural `README.md`.
- **Anti-"Vibe Coding" Authenticity Index (0–100)**:
  - Measures true architecture depth vs. superficial AI-generated code dumps.
  - Heavy penalization if a repository has single-commit 5,000-line drops with "update" messages and zero tests.
- **Repo-Grounded Adaptive Viva Engine**:
  - When generating technical screening tests (`/api/v1/students/generate-test`), the adaptive test engine directly anchors Viva scenarios to the candidate's actual GitHub repositories:
    > *"In your GitHub repository 'distributed-task-queue' (Python, Docker), explain how you architected the data flow and implemented error handling/recovery if a critical dependency fails."*
- **Fairness Guarantee: Dead & Academic Lab Repo Exclusion**:
  - Automatically detects and flags trivial college assignments, lab homework (`lab-`, `assignment-`, `homework-`, `dsa-practice`), and dormant/dead repositories (>2 years abandoned).
  - Excludes toy repositories from technical viva generation (`is_eligible_for_viva=False`) so students are never unfairly penalized or quizzed on first-year college lab exercises.
- **Upfront Showcase Repository Selection & Resource Optimization (`repo_urls` / `selected_repos`)**:
  - Candidates can explicitly provide showcase repository URLs or identifiers beforehand (`POST /students/me/github-sync {"repo_urls": ["https://github.com/alex/my-app", "alex/backend-service"]}`).
  - **Massive Resource & API Quota Savings**: Directly queries `GET /repos/{owner}/{repo}` for specified projects and **completely bypasses exploratory auto-detection** (`GET /users/{username}/repos`), reducing GitHub API calls by 60–80%, avoiding dead/scratchpad repo queries, and preventing rate-limit exhaustion.
  - **Infinite Showcase Repositories Supported**: Zero artificial truncation caps (e.g., no limit to only 3 or 4 repos) — candidates can submit as many showcase repositories as they want ("infinite repos") for full evaluation.
  - **Flexible Identifier Parsing & Auto-Handle Extraction**: Supports full URLs (`https://github.com/owner/repo`), short forms (`owner/repo`), and bare names (`repo`), automatically inferring the candidate's GitHub handle if not explicitly provided.
  - Ensures the adaptive viva specifically targets the architecture the candidate actively stands behind and takes pride in.
- **Skill Evidence & Profile Strength Boost**:
  - Skills verified in candidate's repositories receive a **+15 Project Evidence ($P_e$) boost** in the skills matrix ($W_s$) and are tagged with `is_github_verified=True`.
  - The Candidate Profile Strength Score ($P_{\text{overall}}$) blends verified GitHub engineering scores into $S_{\text{projects\_exp}}$ ($30\%$ weight):
    $$S_{\text{projects\_exp}} = 0.70 \times \overline{W_s} + 0.30 \times \text{engineering\_score}$$
- **Endpoints**:
  - `POST /api/v1/students/me/github-sync`: Trigger public repository analysis (accepts `repo_urls`, `selected_repos`, `github_token`).
  - `GET /api/v1/students/me/github-radar`: Fetch cached engineering radar card.
  - `GET /api/v1/students/generate-test`: Progressive test generation (supports `focus_repo` parameter).
  - Integrated into `GET /api/v1/students/portfolio/me` under `github_engineering_radar`.

---

## 6. Reverse Matching, Recommendations & Upskilling Roadmap

### Features
- **Reverse Matching Engine (`/api/v1/students/recommendations`)**:
  - Dynamically calculates fitment percentages for active job postings against candidate's verified skill matrix ($W_s$).
  - Categorizes openings into match tiers and badges:
    - **Match Percentage** (e.g. `92% Fit`)
    - **Matched Skills Badges** (green)
    - **Missing Skills Badges** (orange)
- **Skill-Gap & Upskilling Roadmap (`/api/v1/students/skill-gap-roadmap`)**:
  - Analyzes market demand frequencies across active employer postings and sector benchmarks.
  - Surfaces prioritized "Skills to Build Next" ranked by market demand.
  - Calculates estimated fitment boost (e.g., *"+18% match boost if you learn Docker"*).
  - Provides actionable multi-domain portfolio project recommendations (e.g., Figma design systems, GST audit checklists in Tally, microservices in Django/FastAPI).
- **Job Discovery Feed (`/api/v1/students/jobs/feed`)**:
  - Filterable by `role_type`, `location`, `is_remote`, `skill_tag`, `is_diversity_drive`, and query `q`. Automatically excludes expired listings.
- **One-Click Direct Application (`/api/v1/students/jobs/{id}/apply`)**:
  - Captures an immutable snapshot of candidate match score and verified skills at the time of application.
  - Protected with `select_for_update` row-level locks and handles deadline expiry.
- **Application Pipeline Tracker (`/api/v1/students/applications`)**:
  - Displays candidate applications with live stage badges (`APPLIED`, `UNDER_REVIEW`, `SHORTLISTED`, `INTERVIEW`, `OFFERED`, `REJECTED`), scheduled interview dates, and full stage transition timeline (`status_history`).

---

## 7. Two-Way 3-Signal Hybrid NLP Search

### Features
- **3-Signal Fusion Algorithm**:
  Combines three distinct algorithmic signals into a weighted composite score:
  1. **Deterministic Skill Overlap (40%)**: Jaccard similarity between candidate skills and job requirements.
  2. **Dense Semantic Vector Similarity (40%)**: Cosine similarity using `BAAI/bge-small-en-v1.5` 384-dimensional embeddings accelerated by PostgreSQL HNSW index.
  3. **Full-Text Keyword SearchRank (20%)**: PostgreSQL `ts_rank` evaluating weighted full-text lexical search vectors (`A: title`, `B: skills`, `C: description`).
- **Recruiter Talent Search (`/api/v1/students/search`)**:
  - Accessible strictly to `RECRUITER` and `ADMIN` tokens.
  - Multipliers for candidate verified cognitive confidence ($CS$) and role-intent alignment.
- **Candidate Conversational Job Search (`/api/v1/listings/search` & `/students/jobs/search`)**:
  - Natural-language search bar allowing candidates to query plain text (e.g., *"remote react frontend engineer with startup equity"*), returning matched jobs, salary brackets, and company branding.

---

## 8. Multi-Domain Affirmative Action & Government Schemes Radar

### Features
- **Cross-Domain Opportunity Coverage**:
  - **Engineering & Tech**: AICTE Pragati Scholarship for Girls (₹50,000/year), Microsoft & SAP TechSaksham, Amazon WOW SDE track, Adobe India WIT ($10,000 grant).
  - **Commerce, Banking & Finance**: ICICI Bank DNA (Diversity Nurturing Academy) Career Fellowship, SEBI & NISM Women in Capital Markets Research Grant.
  - **Management & Business**: Tata Affirmative Action Women Leadership Initiative, P&G Lead With Diversity Fellowship.
  - **Design & Creative Arts**: Adobe Design Circle Global UI/UX Scholarship ($25,000 grant), Women in Animation & Digital Arts (WADA) India Grant.
- **Personalized Eligibility Radar (`/api/v1/students/me/schemes`)**:
  - Cross-references candidate's gender, degree, and CGPA in real-time.
  - Automatically tags qualified opportunities with verified **"100% Eligible"** badges, application countdowns, and direct portal links (`scholarships.gov.in`, `techsaksham.in`).
- **Public Directory (`/api/v1/schemes/live`)**:
  - Public directory enabling faculty mentors and peers to search and share schemes by `domain`, `scheme_type`, `target_gender`, and keyword `q`.
- **Live Status Synchronizer (`/api/v1/schemes/sync-live-status`)**:
  - Scans deadlines, flags expired entries, and dispatches real-time alert notifications to eligible candidates.
- **Corporate Diversity Drives**:
  - Recruiters can tag listings with `is_diversity_drive=True`, `target_gender`, and specific `dei_initiatives` (e.g., mentorship circles, flexible returnships, inclusive childcare).
  - Candidate feed supports `is_diversity_drive=true` filtering.

---

## 9. Candidate Profile Settings & Full Personalization

### Features
- **Settings Management (`GET / PATCH /api/v1/students/me/settings`)**:
  - Granular control over platform features and alert frequencies:
    - **Notifications**: `opportunity_alerts`, `deadline_reminders`, `scheme_alerts`, `application_status_updates`.
    - **Feature Modules**: `show_affirmative_action_schemes`, `show_diversity_job_badges`, `smart_roadmap_recommendations`.
    - **Privacy & Inclusivity**: `participate_in_diversity_hiring`.
- **Total Candidate Agency**:
  - If a student disables `show_affirmative_action_schemes`, the schemes radar cleanly yields 0 schemes without forced segmentation.

---

## 10. Corporate Recruiter Suite & ACID Hiring Pipeline

### Features
- **Enterprise Company Management (`/api/v1/companies/*`)**:
  - Company CRUD with logo URLs, industry verticals, website links, and administrative verification status.
- **Job Posting & Lifecycle (`/api/v1/listings/*`)**:
  - Create, edit, close, and publish listings with salary ranges, work arrangement (remote/hybrid/onsite), experience level, and required skills.
  - Automatic BGE dense vector embedding generation on save.
- **Automated Opportunity Alert Dispatcher**:
  - Publishing a listing automatically scans candidate skill vectors and dispatches `NEW_OPPORTUNITY` alerts via optimized `bulk_create()`.
- **Deadline Approaching Alerts (`/api/v1/students/deadlines/check-reminders`)**:
  - Scans listings expiring within 72 hours and dispatches `DEADLINE_APPROACHING` alerts.
- **Strict ACID Concurrency (`select_for_update`)**:
  - State transitions execute inside `transaction.atomic()` with row-level locks on `JobApplication` and `StudentProfile`.
  - Stages: `APPLIED` $\to$ `UNDER_REVIEW` $\to$ `SHORTLISTED` $\to$ `INTERVIEW` $\to$ `OFFERED` $\to$ `REJECTED`.
  - **Idempotent Transitions**: Retrying an identical transition returns `200 OK` without appending duplicate status history records.
  - **Database Deadlock Defense**: Catches `OperationalError` and returns `409 Conflict` with clear retry messaging under high concurrency.
  - **Ecosystem Placement Sync**: Transitioning to `OFFERED` atomically updates `StudentProfile.placement_status = 'PLACED'`.

---

## 11. Institutional Oversight & Faculty Placement Analytics

### Features
- **Institutional Directory & Departmental Management (`/api/v1/institutions/*`)**:
  - Verified colleges/universities, NIRF rankings, autonomous status, accredited departments, and faculty administrator rosters.
- **Idempotent Placement KPI Overview (`/api/v1/placement/overview`)**:
  - Overview metrics: total eligible cohort, verified placed count, college placement percentage, active hiring partners. Uses `.distinct()` aggregation to prevent double-counting.
- **Branch-Wise Analytics (`/api/v1/placement/branch-wise`)**:
  - Departmental breakdown of placed vs unplaced, highest CTC, and average CTC.
- **Faculty Student Status Roster (`/api/v1/placement/student-status`)**:
  - Pre-fetched student roster (3 constant queries) displaying student offer letters, verified certifications, and profile strength ratings ($P_{\text{overall}}$).
- **Curriculum Skill-Gap Deficit Radar (`/api/v1/placement/skill-gaps`)**:
  - Compares active corporate job requirements against student skills, generating actionable syllabus upgrade recommendations for Academic Councils.
- **In-Demand Skills Radar (`/api/v1/placement/in-demand-skills`)**:
  - Top employer-demanded skills, campus student coverage %, and deficit indices.
- **Recruitment Funnel Trends (`/api/v1/placement/trends`)**:
  - Stage-by-stage conversion funnel and conversion percentages (Applied $\to$ Under Review $\to$ Shortlisted $\to$ Interview $\to$ Offered $\to$ Placed).

---

## 12. Corporate Learning Programs & Hackathon Challenges

### Features
- **Learning Programs Feed (`/api/v1/programs/`)**:
  - Browse corporate upskilling programs, certifications, workshops, and hackathons across partner companies.
  - Filterable by `program_type`, `target_audience`, `mode`, and keyword `q`.
  - Optimized with SQL annotations (1 single query for the entire catalog).
- **Corporate Publishing (`POST /api/v1/programs/`)**:
  - Recruiters publish structured curricula, prerequisites, duration, and certificates.
- **1-Click Universal Enrollment (`POST /api/v1/programs/{id}/enroll`)**:
  - Open to both students/candidates and academicians/faculty.

---

## 13. Faculty Industry Internships, FDPs & Research Collaborations

### Features
- **Faculty Industry Exposure Feed (`/api/v1/institutions/faculty/opportunities`)**:
  - Dedicated search filter for `FACULTY_INTERNSHIP`, `FDP` (Faculty Development Programs), `INDUSTRIAL_TRAINING`, `CONSULTANCY`, `RESEARCH_PROJECT`, `WORKSHOP`, and `GUEST_LECTURE`.
- **Faculty 1-Click Application (`POST /api/v1/institutions/faculty/opportunities/{id}/apply`)**:
  - Faculty submit expressions of interest, research areas, and statements of purpose directly to corporate recruiters.
- **Faculty Collaboration Tracker (`/api/v1/institutions/faculty/my-collaborations`)**:
  - Lists enrolled programs, workshops, and applied FDP tracks for the authenticated faculty member.

---

## 14. Scalability, Database Performance & Resilience Safeguards

### Features
- **HNSW Vector Indexing**:
  - PostgreSQL `pgvector` HNSW indexes active on `skillsetu_student_profiles.embedding` and `skillsetu_job_listings.embedding` (`m=16`, `ef_construction=64`).
  - Delivers sub-3ms approximate nearest neighbor (ANN) retrieval without sequential table scans.
- **Comprehensive N+1 Query Elimination**:
  - Student placement rosters use Django `Prefetch` (3 constant queries for 500 students).
  - Programs feed uses `.annotate()` for count aggregations (1 single query).
  - Opportunity alerts use pre-fetched sets and `bulk_create()`.
  - Upskilling roadmap uses `.only(...)` to defer 384-dimensional vector deserialization during skill-frequency counting.
- **Persistent Connection Pooling & PgBouncer Support**:
  - `CONN_MAX_AGE = 600` (10-minute TCP socket reuse).
  - `CONN_HEALTH_CHECKS = True` (auto-reconnect on dead sockets).
  - `DISABLE_SERVER_SIDE_CURSORS = False` (drop-in compatibility with PgBouncer transaction pooling).
- **State Transition Idempotency**:
  - Duplicate `/apply` calls return existing application record (`200 OK`).
  - Repeated `/status` calls return current state (`200 OK`) without creating duplicate history entries or alerts.
- **Apple-Grade AI Degradation**:
  - Cloud AI service disruptions gracefully trigger deterministic fallbacks for resume extraction and standardized progressive tests with polite system-blame messaging.

---

## 15. Core Mathematical & Anti-Cheat Scoring Formulas

### 1. Individual Skill Proficiency Weight ($W_s$)
Calculated from active project implementation evidence and chronological recency:
$$W_s = (0.6 \times P_e) + (0.4 \times E_r)$$
- **$P_e$ (Project Evidence):** 0–100 score of implementation depth in listed projects.
- **$E_r$ (Experience Recency):** 0–100 score of duration and recency in professional experience.

### 2. Additive Industry Credential Multiplier
If a skill is backed by an active verified industry certification:
$$W_s = \min(100, \text{round}(W_s^{\text{base}} \times 1.15))$$
Tagged with `is_certified=True` and `credential_bonus=1.15`.

### 3. MCQ Linear Time-Decay Multiplier ($M_t$)
Scales correct MCQ answers by candidate response time ($t_s$ in seconds):
- $t_s \le 15\text{s}$: $M_t = 1.0$ (instant recall, 100% score)
- $15 < t_s \le 60\text{s}$: $M_t = 1.0 - 0.3 \times \left(\frac{t_s - 15}{45}\right)$ (linear decay to 70%)
- $t_s > 60\text{s}$: $M_t = 0.7$ (minimum capped score for external search delay)

### 4. Progressive Cognitive Assessment Score ($A_s$)
Combines recall and architectural viva reasoning:
$$A_s = (0.3 \times \text{MCQ average}) + (0.7 \times \text{Viva average})$$

### 5. Capped-Root Plagiarism & Padding Penalty ($CS$)
Penalizes inflated resume claims ($R_s$) against demonstrated knowledge ($A_s$):
$$CS = A_s \times \left(1 - 0.4 \times \sqrt{\frac{\max(0, R_s - A_s)}{100}}\right)$$

### 6. Candidate Profile Strength Score ($P_{\text{overall}}$)
Industry-standard composite score for candidate ranking:
$$P_{\text{overall}} = (0.45 \times S_{\text{cognitive}}) + (0.30 \times S_{\text{projects\_exp}}) + (0.15 \times S_{\text{certifications}}) + (0.10 \times S_{\text{academics}})$$
- **$S_{\text{cognitive}}$ (45%):** Verified confidence score ($CS \in [0, 100]$).
- **$S_{\text{projects\_exp}}$ (30%):** Mean skill proficiency weight ($\overline{W_s} \in [0, 100]$).
- **$S_{\text{certifications}}$ (15%):** Credential tier (1 cert = 70, 2 certs = 85, 3+ certs = 100).
- **$S_{\text{academics}}$ (10%):** Normalized academic score ($(\text{CGPA} / 10.0) \times 100$).

---

## 16. Complete API Endpoint Catalog

### Authentication (`/api/v1/auth`)
| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | None | Register new user account with role |
| `POST` | `/auth/login` | None | Standard username/password login, returns 24h JWT |
| `GET` | `/auth/me` | JWT | Get current authenticated user profile & avatar |
| `GET` | `/auth/oauth/urls` | None | Get pre-configured Google & GitHub OAuth redirect URLs |
| `POST` | `/auth/oauth/login` | None | Universal OAuth token exchange & auto-provisioning |

### Student Screening, Testing & Portfolio (`/api/v1/students`)
| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/students/resume-preview-extract` | None | In-memory resume extraction preview without saving |
| `POST` | `/students/upload-resume` | Student | Upload resume, parse skills & calculate fitment matrix |
| `GET` | `/students/profile/me` | Student | Retrieve own candidate profile & skills matrix |
| `POST` | `/students/generate-test` | Student | Generate 5 progressive questions for target role |
| `POST` | `/students/submit-test` | Student | Submit test, trigger anti-cheat evaluation & update CS |
| `GET` | `/students/portfolio/me` | Student | Get own comprehensive digital portfolio |
| `GET` | `/students/{id}/portfolio` | Public/Recruiter | Get candidate portfolio (supports `?blind=true`) |
| `GET` | `/students/me/nep-transcript` | Student | Export signed DigiLocker/ABC academic credit transcript |
| `POST` | `/students/me/github-sync` | Student | Screen public GitHub profile & compute engineering radar |
| `GET` | `/students/me/github-radar` | Student | Get candidate cached GitHub engineering & anti-vibe radar |
| `POST` | `/students/internships/{id}/log-milestone` | Student | Log weekly internship milestone progress |
| `GET` | `/students/search` | Recruiter | 3-Signal hybrid candidate search (BGE vector + HNSW) |

### Job Discovery, Recommendations & Roadmaps (`/api/v1/students`)
| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/students/jobs/feed` | None/Student | Active openings feed (filter by role, location, DEI) |
| `GET` | `/students/jobs/search` | None/Student | Natural-language conversational job search |
| `GET` | `/students/recommendations` | Student | Personalized reverse-matched job recommendations |
| `GET` | `/students/skill-gap-roadmap` | Student | Actionable upskilling roadmap & market skill deficits |
| `POST` | `/students/jobs/{id}/apply` | Student | One-click direct application with row locking |
| `GET` | `/students/applications` | Student | Track active applications & status history pipeline |
| `GET` | `/students/notifications` | Student | Retrieve real-time candidate notifications |
| `GET` | `/students/deadlines` | Student | Approaching application deadlines calendar |
| `POST` | `/students/deadlines/check-reminders` | Student/Admin | Scan and dispatch 72-hour deadline alerts |

### Diversity & Affirmative Action Schemes (`/api/v1`)
| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/schemes/live` | None | Public directory of live multi-domain government schemes |
| `GET` | `/students/me/schemes` | Student | Candidate personalized schemes radar ("100% Eligible") |
| `POST` | `/schemes/sync-live-status` | None/Admin | Sync deadline status & dispatch scheme alerts |
| `GET` | `/students/me/settings` | Student | Get candidate personal settings (common, career discovery, privacy, features) |
| `PUT/PATCH` | `/students/me/settings` | Student | Update candidate settings with section merging |

### Recruiter & Enterprise Job Engine (`/api/v1`)
| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/recruiters/me` | Recruiter | Get recruiter profile and active preferences |
| `PUT` | `/recruiters/me` | Recruiter | Update recruiter profile |
| `GET` | `/recruiters/me/settings` | Recruiter | Get recruiter workflow, screening, and alert preferences |
| `PUT/PATCH` | `/recruiters/me/settings` | Recruiter | Update recruiter settings (blind screening default, engineering filter) |
| `GET` | `/companies/` | None/Recruiter | List verified partner companies |
| `POST` | `/companies/` | Recruiter | Register a new partner company |
| `GET` | `/companies/{id}` | None/Recruiter | Get company profile & active openings |
| `GET` | `/listings/` | None/Recruiter | List all active job postings |
| `POST` | `/listings/` | Recruiter | Post new job listing (auto-generates BGE vector) |
| `GET` | `/listings/{id}` | None/Recruiter | Detailed job description & requirements |
| `PATCH` | `/listings/{id}` | Recruiter | Update job listing details |
| `POST` | `/listings/{id}/close` | Recruiter | Close job listing to new applicants |
| `GET` | `/listings/search` | None/Student | 3-Signal hybrid job search |
| `GET` | `/applications/listings/{id}/applications` | Recruiter | List applicants for listing (supports `?blind=true`) |
| `POST` | `/applications/{id}/status` | Recruiter | ACID state transition with row locking |
| `POST` | `/applications/{id}/internship-progress` | Recruiter | Record mentor evaluation, star rating & certificate |

### Corporate Learning Programs & Challenges (`/api/v1/programs`)
| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/programs/` | None/Auth | List corporate learning programs & hackathons |
| `POST` | `/programs/` | Recruiter | Publish new training program / hackathon |
| `GET` | `/programs/{id}` | None/Auth | Program syllabus, timeline & certificate details |
| `POST` | `/programs/{id}/enroll` | Student/Faculty | 1-Click universal program enrollment |

### Institutional Placement Analytics (`/api/v1/placement`)
| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/placement/overview` | Academia | Idempotent college placement overview KPIs |
| `GET` | `/placement/branch-wise` | Academia | Branch-wise placement percentages & CTC stats |
| `GET` | `/placement/student-status` | Academia | Pre-fetched student roster with offer details |
| `GET` | `/placement/skill-gaps` | Academia | Departmental skill-gap radar & syllabus suggestions |
| `GET` | `/placement/in-demand-skills` | Academia | Top employer-demanded skills & coverage deficits |
| `GET` | `/placement/trends` | Academia | Recruitment funnel stage-by-stage conversion |

### Institutions & Faculty Collaboration (`/api/v1/institutions`)
| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/institutions/directory` | None | Verified colleges & universities directory |
| `POST` | `/institutions/` | Academia/Admin | Register new academic institution |
| `POST` | `/institutions/{id}/departments` | Academia | Add department to institution |
| `GET` | `/institutions/faculty/me` | Academia | Get authenticated faculty profile |
| `PATCH` | `/institutions/faculty/me` | Academia | Update faculty research areas & profile |
| `GET` | `/institutions/faculty/me/settings` | Academia | Get institutional TPO placement alerts & radar preferences |
| `PUT/PATCH` | `/institutions/faculty/me/settings` | Academia | Update faculty preferences (skill deficit alert, DigiLocker auto-sync) |
| `GET` | `/institutions/faculty/opportunities` | Academia | Discover faculty internships, FDPs & consultancies |
| `POST` | `/institutions/faculty/opportunities/{id}/apply` | Academia | Apply for faculty industry exposure program |
| `GET` | `/institutions/faculty/my-collaborations` | Academia | Track applied FDPs & faculty industry engagements |
