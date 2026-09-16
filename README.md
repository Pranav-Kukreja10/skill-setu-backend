# Skill Setu — AI-Powered Skill Verification, Job Engine & Institutional Placement Platform

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2](https://img.shields.io/badge/django-5.2%20LTS-green.svg)](https://www.djangoproject.com/)
[![Django Ninja](https://img.shields.io/badge/django--ninja-fastapi%20speed-teal.svg)](https://django-ninja.dev/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-pgvector%20384d-blue.svg)](https://github.com/pgvector/pgvector)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini%20Flash%20Lite-orange.svg)](https://ai.google.dev/)
[![Ollama Local](https://img.shields.io/badge/GPU%20Fallback-Ollama%20Qwen3.5-purple.svg)](https://ollama.ai/)

**Skill Setu** is an enterprise-grade, contract-first backend ecosystem designed for the **Smart India Hackathon (SIH)** problem statement: *"Portal for Academia – Industry collaboration for Skill Mapping, Internships and Placement"*. It seamlessly connects students, corporate recruiters, and academic faculty through automated skill verification, adaptive cognitive assessments, anti-cheat plagiarism deterrence, two-way NLP hybrid search, blind hiring workflows, live internship progress tracking, industry learning programs, and institutional skill-gap analytics.

---

## 🏆 Verbatim SIH Problem Statement Compliance Matrix

Designed to withstand the most rigorous evaluation, every clause of the SIH Problem Statement is implemented with concrete database models, mathematical formulas, and verified REST API endpoints:

| SIH Problem Statement Requirement | Platform Feature & Implementation | Domain & Models | API Endpoints & Contracts | Verification Status |
|---|---|---|---|---|
| **Student Registration & Profiling** | Multi-domain profile creation with academic credentials, CGPA, graduation year, social links, resume parsing | `accounts.User`<br>`students.StudentProfile` | `POST /api/v1/auth/register`<br>`GET /api/v1/students/me`<br>`PUT /api/v1/students/me` | **100% Verified** |
| **Skill Mapping Engine** | Capturing and structuring technical, frameworks, tools, and soft skills with evidence weight $W_s = 0.6 P_e + 0.4 E_r$ | `students.services`<br>`JobBenchmark` | `POST /api/v1/students/resume-preview-extract`<br>`POST /api/v1/students/analyze-resume` | **100% Verified** |
| **Student Digital Portfolio** | Comprehensive portfolio aggregating verified skills ($W_s$), cognitive scores ($A_s$), certifications, projects, internships, achievements, transcripts | `StudentProfile.internships`<br>`StudentProfile.achievements`<br>`StudentProfile.academic_records` | `GET /api/v1/students/portfolio/me`<br>`GET /api/v1/students/{id}/portfolio`<br>`PUT /api/v1/students/portfolio/achievements` | **100% Verified** |
| **Industry/Recruiter Registration & Company Profile** | Partner company verification, branding logos, recruiter profile management | `recruiters.Company`<br>`recruiters.RecruiterProfile` | `POST /api/v1/auth/register`<br>`GET /api/v1/recruiters/me`<br>`POST /api/v1/recruiters/company` | **100% Verified** |
| **Internship & Job Management** | Multi-target listing management across full-time, student internships, apprenticeships, live projects | `recruiters.JobListing` | `POST /api/v1/listings/`<br>`GET /api/v1/listings/my-listings`<br>`GET /api/v1/listings/{id}` | **100% Verified** |
| **Application & Shortlisting Workflow** | One-click apply with ACID row locking (`select_for_update`), stage history audit trail, automatic placement sync | `recruiters.JobApplication` | `POST /api/v1/students/jobs/{id}/apply`<br>`PATCH /api/v1/applications/{id}/status`<br>`GET /api/v1/students/applications` | **100% Verified** |
| **Internship Progress Tracking & Milestone Logs** | Student weekly milestone progress logs (week #, summary, hours, deliverables URL) and live status tracking | `JobApplication.weekly_progress_logs`<br>`JobApplication.internship_status` | `GET /api/v1/students/internships/active`<br>`POST /api/v1/students/internships/{id}/log-milestone` | **100% Verified** |
| **Mentor Feedback & Rating Supervision** | Recruiter/mentor supervision, logging qualitative review remarks, 1-5 star performance rating, completion certificates | `JobApplication.mentor_feedback`<br>`JobApplication.mentor_rating`<br>`JobApplication.completion_certificate_url` | `PATCH /api/v1/applications/{id}/internship-progress` | **100% Verified** |
| **Faculty Internships & FDPs** | Dedicated exposure discovery for academicians: Faculty Internships, FDPs, Industrial Training, Research Projects, Consultancies | `JobListing.role_type`<br>`JobListing.target_audience="FACULTY"` | `GET /api/v1/institutions/faculty/opportunities`<br>`POST /api/v1/institutions/faculty/opportunities/{id}/apply` | **100% Verified** |
| **Industry Learning Programs & Workshops** | Corporate training programs, certification courses, hands-on workshops, mentorship initiatives, innovation challenges / hackathons | `recruiters.LearningProgram` | `GET /api/v1/programs/`<br>`POST /api/v1/programs/`<br>`GET /api/v1/programs/{id}`<br>`POST /api/v1/programs/{id}/enroll` | **100% Verified** |
| **Blind Screening for Objective Hiring** | `blind=True` toggle redacting candidate PII (name $\to$ `"Candidate #ID"`, email/college $\to$ `[REDACTED]`) while preserving verified skills matrix and credentials | `students.search`<br>`recruiters.api` | `GET /api/v1/students/search?blind=true`<br>`GET /api/v1/listings/{id}/applicants?blind=true`<br>`GET /api/v1/students/{id}/portfolio?blind=true` | **100% Verified** |
| **Institutional Placement Oversight & Reporting** | Idempotent institutional metrics: total placement percentage, branch-wise metrics, student offer letter rosters | `institutions.api`<br>`distinct().count()` | `GET /api/v1/placement/overview`<br>`GET /api/v1/placement/branch-wise`<br>`GET /api/v1/placement/student-status` | **100% Verified** |
| **Skill-Gap Visibility & Curriculum Radar** | Departmental skill deficit analytics comparing industry demand vs student supply, surfacing actionable syllabus recommendations | `institutions.api`<br>`SkillGapAnalysisOut` | `GET /api/v1/placement/skill-gaps`<br>`GET /api/v1/placement/in-demand-skills` | **100% Verified** |
| **Notifications & Approaching Deadlines** | Real-time alerts for opportunities, status changes, scheduled interviews, and 72-hour expiring deadline reminders | `students.Notification` | `GET /api/v1/students/notifications`<br>`GET /api/v1/students/deadlines`<br>`POST /api/v1/students/deadlines/check-reminders` | **100% Verified** |

---

## 🌟 Key Platform Features

### 1. Universal Multi-Domain Candidate Profiling
- **Cross-Disciplinary Coverage:** Beyond traditional software engineering, dynamically parses, benchmarks, and scores candidates across:
  - **Commerce & Accounting (B.Com, M.Com, CA, CMA):** Tally Prime, GST, TDS, Statutory Auditing, GAAP/IFRS, QuickBooks, Financial Modeling.
  - **Business Administration (BBA, MBA, PGDM):** Business Analysis, Market Sizing, SWOT, Supply Chain, Operations, CRM (Salesforce).
  - **Design & Creative Arts (B.Des, M.Des, UI/UX):** Figma Design Systems, User Journeys, Wireframing, WCAG Accessibility, Adobe Creative Suite.
  - **Engineering & Technology (B.Tech, BE, BCA, MCA):** Full-Stack, Distributed Systems, Cloud Architecture, CAD/FEA Simulation.
- **Dynamic 4-Tier Categorization:** Parses resume text into `technical_skills`, `frameworks`, `tools`, and `soft_skills`.
- **Inclusive Candidate Roles:** Full feature parity across `STUDENT`, `CANDIDATE` (graduates & experienced job seekers), `RECRUITER`, and `ACADEMIA` (faculty).

### 2. Comprehensive Candidate Profile Strength Scoring ($P_{\text{overall}}$)
Evaluates candidates using an industry-standard weighted composite score:
$$P_{\text{overall}} = (0.45 \times S_{\text{cognitive}}) + (0.30 \times S_{\text{projects\_exp}}) + (0.15 \times S_{\text{certifications}}) + (0.10 \times S_{\text{academics}})$$
- **$S_{\text{cognitive}}$ (45%):** Verified confidence score ($CS \in [0, 100]$) achieved in proctored assessments.
- **$S_{\text{projects\_exp}}$ (30%):** Weighted mean skill proficiency weight ($\overline{W_s} \in [0, 100]$) derived from hands-on projects and professional recency.
- **$S_{\text{certifications}}$ (15%):** Structured credential rating (1 cert = 70, 2 certs = 85, 3+ certs = 100).
- **$S_{\text{academics}}$ (10%):** Normalized academic record ($(\text{CGPA} / 10.0) \times 100$).

### 3. Additive Credential Multiplier
- Skills backed by verified industry certifications receive an automatic **+15% proficiency boost**:
  $$W_s = \min(100, \text{round}(W_s^{\text{base}} \times 1.15))$$
- Marked with `is_certified=True` and `credential_bonus=1.15`, directly boosting fitment rankings.

### 4. Anti-Cheat Adaptive Testing & Plagiarism Penalties
- **Linear Time-Decay Multiplier ($M_t$):** Dynamically scales MCQ points based on response speed ($t_s$), differentiating instant mastery from external search delay:
  - $t_s \le 15\text{s} \implies 1.0$ (no penalty)
  - $15\text{s} < t_s \le 60\text{s} \implies 1.0 - 0.3 \times \frac{t_s - 15}{45}$ (linear decay to 70%)
  - $t_s > 60\text{s} \implies 0.7$ (capped minimum)
- **Progressive Cognitive Score ($A_s$):** Combines syntax recall and architectural viva reasoning:
  $$A_s = (0.3 \times \text{MCQ average}) + (0.7 \times \text{Viva average})$$
- **Plagiarism & Resume Padding Penalty ($CS$):** Abnormally high gaps between resume claims ($R_s$) and test scores ($A_s$) trigger a non-linear square-root penalty:
  $$CS = A_s \times \left(1 - 0.4 \times \sqrt{\frac{\max(0, R_s - A_s)}{100}}\right)$$

### 5. Two-Way 3-Signal Hybrid NLP Search
- **Recruiter Candidate Search (`/api/v1/students/search`):** Fuses deterministic skill overlap, dense 384-dimensional BGE cosine vector similarity, and PostgreSQL full-text SearchRank, modulated by candidate cognitive confidence.
- **Candidate Job Search (`/api/v1/listings/search`):** Natural language search across active postings matching conversational queries, compensation, location, and technical badges.

### 6. Recruiter Engine & ACID Application Pipeline
- **Strict Row Locking (`select_for_update`):** All application transitions (`APPLIED` $\to$ `UNDER_REVIEW` $\to$ `SHORTLISTED` $\to$ `INTERVIEW` $\to$ `OFFERED` $\to$ `REJECTED`) run in atomic blocks with row-level locks and HTTP 409 Conflict handlers.
- **Automatic Placement Sync:** Advancing a candidate to `OFFERED` atomically updates the student's status to `PLACED`.
- **Blind Screening Toggle (`blind=True`):** Masks candidate names, emails, and institutions while preserving verified skill matrices, certifications, projects, and cognitive ratings for unbiased merit hiring.

### 7. Real-Time Opportunity & Deadline Alerts
- **Opportunity Alerts (`NEW_OPPORTUNITY`):** Automatically scans matching candidate skill profiles upon publishing any job listing and dispatches instant in-app alerts.
- **Approaching Deadline Reminders (`DEADLINE_APPROACHING`):** Periodic and on-demand scanner (`POST /api/v1/students/deadlines/check-reminders`) alerts matching candidates whose target openings expire within 72 hours.

### 8. Institutional Faculty Analytics & Oversight (`/api/v1/placement/*`)
- **Skill-Gap Deficit Radar (`/placement/skill-gaps`):** Visualizes departmental market demand vs student supply, computing deficit percentages and actionable curriculum recommendations.
- **In-Demand Skills Trends (`/placement/in-demand-skills`):** Tracks employer demand, student coverage, and hiring sector distributions.
- **Recruitment Funnel Velocities (`/placement/trends`):** Conversion rates across all hiring stages and contract distributions.
- **Idempotent Reporting:** Employs distinct aggregation sets (`.values('student_id').distinct().count()`) to guarantee reliable institutional statistics regardless of network retries.

### 9. Task-Specific AI Routing & Local GPU Fallback
- **Task-Specific Cloud Routing:**
  - Resume Parsing: `gemini-3.1-flash-lite`
  - Adaptive Question Generation: `gemini-3.5-flash-lite`
  - Viva Rubric Grading: `gemini-3.1-flash-lite`
- **Zero-Crash Resilience:** 120-second timeout handling cloud API latency spikes.
- **Instant GPU Fallback:** Set `AI_PROVIDER=local` in `.env` to redirect all AI workloads to a local Ollama instance (`qwen3.5:9b`).

---

## 📐 Architecture & System Workflow Diagrams

### 1. End-to-End System Data Flow
```mermaid
graph TD
    A[Candidate: Upload Resume] --> B[In-Memory Text Extraction: pypdf / python-docx]
    B --> C[Cloud AI Gateway: Gemini Flash Lite / Local GPU Ollama]
    C --> D[Dynamic 4-Tier Categorization & Skills Matrix Ws]
    D --> E[Benchmark Fitment Engine: Sector & Role Matching]
    E --> F[Adaptive Test Generator: 5 Progressive Questions]
    F --> G[Real-Time Grader: MCQ Time Decay + Viva Rubric]
    G --> H[Plagiarism & Resume Padding Penalty CS Engine]
    H --> I[Profile Strength Scoring P_overall + 15% Credential Boost]
    I --> J[PostgreSQL + pgvector 384d Dense Embedding]
    J --> K[Two-Way 3-Signal Hybrid Matcher]
    K --> L[Recruiter Engine: Blind & Unbiased Review]
    L --> M[ACID select_for_update Hiring Pipeline]
    M --> N[Faculty Placement & Skill-Gap Analytics Radar]
```

### 2. ACID Application Lifecycle & State Machine
```mermaid
stateDiagram-v2
    [*] --> APPLIED : One-Click Direct Apply
    APPLIED --> UNDER_REVIEW : Recruiter Review (select_for_update)
    UNDER_REVIEW --> SHORTLISTED : Candidate Shortlisted
    SHORTLISTED --> INTERVIEW : Schedule Interview Date
    INTERVIEW --> OFFERED : Job Offered (Atomic Row Lock)
    OFFERED --> PLACED : Student Placement Status Updated
    APPLIED --> REJECTED : Application Declined
    UNDER_REVIEW --> REJECTED
    SHORTLISTED --> REJECTED
    INTERVIEW --> REJECTED
```

---

## 🏗️ Architecture & Directory Structure

```text
skillsetu-backend/
├── .env                              # Environment credentials & model routing
├── .env.example                      # Sanitized environment configuration blueprint
├── manage.py                         # Django administrative command CLI
├── requirements.txt                  # Python production dependencies
├── skillsetu_backend/
│   ├── api.py                        # Central Django Ninja API router & docs
│   ├── settings.py                   # PostgreSQL, CORS, JWT & pgvector settings
│   └── urls.py                       # Root endpoint routing
├── accounts/                         # Modular identity & authentication domain
│   ├── api.py                        # Registration, login, token refresh
│   ├── models.py                     # Custom user roles (Student, Candidate, Recruiter, Faculty)
│   ├── schemas.py                    # Pydantic schemas for auth
│   └── security.py                   # Role-based JWT authenticators (StudentAuth, RecruiterAuth, AcademiaAuth)
├── students/                         # Candidate profiling, assessments & search
│   ├── management/commands/
│   │   ├── seed_benchmarks.py        # Multi-domain industry benchmarks seeder
│   │   ├── seed_data.py              # Candidate test profiles seeder
│   │   └── reindex_profiles.py       # Rebuilds search vectors & BGE embeddings
│   ├── api.py                        # Profiles, resume preview, test generation & grading
│   ├── models.py                     # StudentProfile, TestSession, Notification
│   ├── services.py                   # In-memory document extractors & scoring engines
│   ├── grader.py                     # MCQ time-decay and Gemini viva grading engine
│   ├── ai_gateway.py                 # Task-specific model router & load balancer
│   ├── recommendations.py            # Personalized reverse matching & upskilling roadmap
│   └── search.py                     # 3-signal candidate hybrid search
├── recruiters/                       # Recruiter engine, jobs & applicant pipeline
│   ├── management/commands/
│   │   └── seed_recruiter_data.py    # Seed partner companies, recruiters & job postings
│   ├── api.py                        # Company CRUD, job lifecycle, ACID applications
│   ├── models.py                     # Company, RecruiterProfile, JobListing, JobApplication
│   ├── schemas.py                    # Job posting, applicant review & candidate search schemas
│   └── search.py                     # Candidate NLP job search engine
└── institutions/                     # Dedicated academia, institutional oversight & analytics domain
    ├── management/commands/
    │   └── seed_institutions.py      # Seed verified colleges/universities, departments & faculty
    ├── api.py                        # Institutions directory, faculty profile, skill-gaps & placement radar
    ├── models.py                     # Institution, Department, FacultyProfile
    └── schemas.py                    # Institutional profiling, departmental analytics & trends
```

---

## 🚀 Quickstart & Installation

### Prerequisites
- **Python:** `3.11.9`
- **PostgreSQL:** `15+` with `pgvector` extension enabled
- **Git**

---

### 1. Clone the Repository
```bash
git clone https://github.com/Pranav-Kukreja10/skill-setu-backend.git
cd skill-setu-backend
```

---

### 2. Configure Virtual Environment

**Windows (PowerShell):**
```powershell
py -3.11 -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables
Copy the template `.env.example` to `.env` and fill in your credentials:
```bash
copy .env.example .env     # Windows
cp .env.example .env       # macOS / Linux
```

Edit `.env`:
```env
DEBUG=True
SECRET_KEY=your-django-secret-key-here

# PostgreSQL Settings
DB_NAME=skillsetu_db
DB_USER=skillsetu_user
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

# AI Routing (Options: cloud | local | mock)
AI_PROVIDER=cloud
GEMINI_API_KEY=your-gemini-api-key

# Optional: Local GPU settings (if AI_PROVIDER=local)
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3.5:9b
```

---

### 5. Initialize Database & Run Seeders
Run migrations and load the multi-domain benchmark and test datasets:
```bash
# 1. Run migrations
python manage.py migrate

# 2. Seed multi-domain industry benchmarks (Tech, Finance, HR, Design)
python manage.py seed_benchmarks

# 3. Seed student & candidate profiles with verified skill matrices
python manage.py seed_data

# 4. Seed partner companies, recruiters, and vector-indexed postings
python manage.py seed_recruiter_data

# 5. Seed verified institutions (Universities, IITs/NITs), departments & faculty
python manage.py seed_institutions

# 6. (Optional) Rebuild BGE pgvector embeddings and search corpora
python manage.py reindex_profiles
```

---

### 6. Start the Development Server
```bash
python manage.py runserver
```
The backend API is now live at: `http://127.0.0.1:8000`

---

## 📖 API Documentation & Endpoints

Interactive OpenAPI Swagger documentation is available out-of-the-box:
- **Swagger UI:** [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)
- **OpenAPI Schema:** [http://127.0.0.1:8000/api/v1/openapi.json](http://127.0.0.1:8000/api/v1/openapi.json)

### Key Endpoint Index

| Domain | Method | Endpoint | Description | Auth Required |
|---|---|---|---|---|
| **Auth** | `POST` | `/api/v1/auth/register` | Register Student, Recruiter, or Faculty | None |
| **Auth** | `POST` | `/api/v1/auth/login` | Login and acquire JWT access token | None |
| **Candidate** | `GET` | `/api/v1/students/me` | Fetch verified profile, $P_{\text{overall}}$, & skills | Student/Candidate |
| **Candidate** | `PUT` | `/api/v1/students/me` | Update academics, social links, certifications | Student/Candidate |
| **Candidate** | `POST` | `/api/v1/students/resume-preview-extract` | In-memory resume parse preview | Student/Candidate |
| **Candidate** | `POST` | `/api/v1/students/analyze-resume` | Commit resume parse to skills matrix ($W_s$) | Student/Candidate |
| **Assessment** | `POST` | `/api/v1/students/generate-test` | AI-generated adaptive 5-question viva + MCQ | Student/Candidate |
| **Assessment** | `POST` | `/api/v1/students/submit-test` | Time-decay MCQ & viva grading, CS update | Student/Candidate |
| **Discovery** | `GET` | `/api/v1/students/jobs/feed` | Active job openings feed with filters | Student/Candidate |
| **Discovery** | `POST` | `/api/v1/students/jobs/search` | Natural language 3-signal job search | Student/Candidate |
| **Discovery** | `GET` | `/api/v1/students/recommendations` | Reverse-matching personalized feed | Student/Candidate |
| **Discovery** | `GET` | `/api/v1/students/skill-gap-roadmap` | Priority skills & project roadmap | Student/Candidate |
| **Applications** | `POST` | `/api/v1/students/jobs/{id}/apply` | ACID 1-click application submission | Student/Candidate |
| **Applications** | `GET` | `/api/v1/students/applications` | Student application status tracking | Student/Candidate |
| **Recruiter** | `GET` | `/api/v1/recruiters/company` | Fetch or create company profile | Recruiter |
| **Recruiter** | `POST` | `/api/v1/listings/` | Create & publish new job listing | Recruiter |
| **Recruiter** | `GET` | `/api/v1/students/search` | 3-signal talent search (vector + keyword) | Recruiter/Admin |
| **Recruiter** | `GET` | `/api/v1/listings/{id}/applicants` | Review applicants (`blind=true` toggle) | Recruiter |
| **Recruiter** | `PATCH`| `/api/v1/applications/{id}/status` | ACID stage transition (`select_for_update`) | Recruiter |
| **Academia** | `GET` | `/api/v1/institutions/directory` | Public directory of verified colleges & departments | None |
| **Academia** | `POST` | `/api/v1/institutions/` | Register new college / institution | Faculty / Admin |
| **Academia** | `POST` | `/api/v1/institutions/{id}/departments` | Add academic department | Faculty / Admin |
| **Academia** | `GET` | `/api/v1/institutions/faculty/me` | Faculty profile & institution info | Faculty |
| **Academia** | `PUT` | `/api/v1/institutions/faculty/me` | Update faculty profile & designation | Faculty |
| **Placement** | `GET` | `/api/v1/placement/overview` | Institutional placement statistics | Faculty |
| **Placement** | `GET` | `/api/v1/placement/skill-gaps` | Departmental skill-gap deficit radar | Faculty |
| **Placement** | `GET` | `/api/v1/placement/in-demand-skills` | Market demand & deficit analytics | Faculty |
| **Placement** | `GET` | `/api/v1/placement/trends` | Recruitment funnel conversion metrics | Faculty |
| **Placement** | `GET` | `/api/v1/placement/student-status` | Student placement roster & certifications | Faculty |


---

## 👥 Pre-Seeded Demo Personas & Credentials

For immediate testing, hackathon evaluation, and frontend integration, the following multi-domain accounts are pre-seeded with rich skill profiles and listings:

| Persona / Role | Username | Password | Organization / Specialization | Recommended Test Workflows |
|---|---|---|---|---|
| **Tech Candidate** | `alex_dev` | `password123` | B.Tech CS, Backend Systems (Python, Django, AWS) | Feed discovery, 3-signal job search, reverse matching, one-click apply |
| **Finance Candidate** | `ananya_fin` | `password123` | Commerce / Finance (DCF, Valuation, Financial Modeling) | Cross-domain multi-discipline fitment, upskilling roadmap |
| **Mechanical Candidate** | `rahul_cad` | `password123` | Mechanical Engineering (SolidWorks, ANSYS, FEA) | Multi-domain CAD benchmark matching, profile strength review |
| **Tech Recruiter** | `recruiter_google` | `password123` | Google India (Core Infrastructure) | Publish listings, 3-signal talent search, blind applicant review, status changes |
| **Industrial Recruiter** | `recruiter_tata` | `password123` | Tata Motors (Automotive R&D) | Automotive & mechanical applicant evaluation |
| **Institutional Faculty** | `faculty_dean` | `password123` | University Placement Cell | Departmental skill deficit radar, in-demand skills trends, recruitment funnel |

---

## 🐳 1-Click Docker Deployment

Run the complete stack (PostgreSQL with `pgvector`, Django Ninja backend, automated migrations, and seed datasets) with a single command:

```bash
docker compose up --build
```
- **Backend API Docs:** `http://localhost:8000/api/v1/docs`
- **PostgreSQL Database:** `localhost:5432` with pre-installed `pgvector/pgvector:pg16`

---

## 🧪 Running Automated Unit Tests

Run the platform test suite:
```bash
python manage.py test students institutions
```
Verifies:
- Skill proficiency weight calculation ($W_s$)
- Additive +15% credential boost on certified skills
- MCQ linear time-decay multiplier ($M_t$)
- Progressive cognitive assessment score ($A_s$)
- Non-linear plagiarism & resume padding confidence penalty ($CS$)
- Overall candidate profile strength score ($P_{\text{overall}}$)
- Institution, department, and faculty profile contracts
- Placement overview, skill-gap deficit, and market demand schemas

---

## 📡 Quick API Request & Response Examples

### 1. User Authentication (`POST /api/v1/auth/login`)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "alex_dev", "password": "password123"}'
```
**Response:**
```json
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "alex_dev",
    "role": "STUDENT"
  }
}
```

### 2. Candidate 3-Signal Natural Language Job Search (`POST /api/v1/students/jobs/search`)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/students/jobs/search" \
  -H "Authorization: Bearer <STUDENT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query": "Python and Django backend engineer remote or hybrid", "limit": 5}'
```

### 3. Recruiter Blind Candidate Review (`GET /api/v1/listings/{id}/applicants?blind=true`)
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/listings/1/applicants?blind=true" \
  -H "Authorization: Bearer <RECRUITER_TOKEN>"
```
**Response (PII Redacted for Unbiased Merit Hiring):**
```json
[
  {
    "application_id": 9,
    "status": "APPLIED",
    "snapshot_match_score": 0.88,
    "candidate": {
      "candidate_identifier": "Candidate #24",
      "email": "[REDACTED]",
      "institution": "[REDACTED]",
      "profile_strength_score": 78.25,
      "certifications": [{"name": "AWS Certified Solutions Architect", "issuer": "AWS"}],
      "skills_matrix": {"python": {"weight": 88}, "aws": {"weight": 83, "is_certified": true}}
    }
  }
]
```

### 4. Faculty Departmental Skill-Gap Radar (`GET /api/v1/placement/skill-gaps`)
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/placement/skill-gaps?department=Computer%20Science" \
  -H "Authorization: Bearer <FACULTY_TOKEN>"
```


---

## 💻 Connecting with Frontend (Smoke Test)

To test end-to-end integration with a React/Vite client:

### 1. Initialize Vite Project
```bash
npm create vite@latest skillsetu-frontend -- --template react
cd skillsetu-frontend
npm install axios @tanstack/react-query
```

### 2. Configure Environment Variable
In `skillsetu-frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 3. Verification Smoke Test (`src/App.jsx`)
```jsx
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL });

export default function App() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['students'],
    queryFn: async () => (await api.get('/students/')).data,
  });

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Skill Setu — Integration Test</h1>
      {isLoading && <p>Connecting to backend API...</p>}
      {isError && <p style={{ color: 'red' }}>Connection failed: {error.message}</p>}
      {data && (
        <div>
          <p style={{ color: 'green', fontWeight: 'bold' }}>✓ Successfully connected to Django Ninja API!</p>
          <pre style={{ background: '#f4f4f4', padding: '1rem', borderRadius: '6px' }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}
```

Run `npm run dev` to verify real-time communication:

![Skill Setu Integration Test](image.png)

---

## 📡 Complete REST API Surface Catalog

| Group | Method | Endpoint | Description | Guard / Security |
|---|---|---|---|---|
| **Auth** | `POST` | `/api/v1/auth/register` | Register new Student, Candidate, Recruiter, Faculty | Public |
| **Auth** | `POST` | `/api/v1/auth/login` | Acquire JWT access and refresh tokens | Public |
| **Candidate** | `GET` | `/api/v1/students/me` | Fetch verified profile, $P_{\text{overall}}$, and $W_s$ | StudentAuth / CandidateAuth |
| **Candidate** | `PUT` | `/api/v1/students/me` | Update academics, certifications, social links, achievements | StudentAuth / CandidateAuth |
| **Candidate** | `POST` | `/api/v1/students/resume-preview-extract` | In-memory resume preview without database commit | StudentAuth / CandidateAuth |
| **Candidate** | `POST` | `/api/v1/students/analyze-resume` | Commit resume parse into skills matrix ($W_s$) | StudentAuth / CandidateAuth |
| **Portfolio** | `GET` | `/api/v1/students/portfolio/me` | Complete Digital Portfolio (skills, scores, certs, projects, achievements, transcripts) | StudentAuth / CandidateAuth |
| **Portfolio** | `GET` | `/api/v1/students/{id}/portfolio` | Candidate portfolio review (`blind=true` toggle support) | JWTAuth |
| **Portfolio** | `PUT` | `/api/v1/students/portfolio/achievements` | Update verified achievements & honors | StudentAuth / CandidateAuth |
| **Assessment** | `POST` | `/api/v1/students/generate-test` | Progressive 5-question viva + MCQ generation | StudentAuth / CandidateAuth |
| **Assessment** | `POST` | `/api/v1/students/submit-test` | Time-decay MCQ & viva grading, CS confidence update | StudentAuth / CandidateAuth |
| **Candidate** | `GET` | `/api/v1/students/jobs/feed` | Filterable active jobs feed (role, location, remote) | StudentAuth / CandidateAuth |
| **Candidate** | `POST` | `/api/v1/students/jobs/search` | Plain-language 3-signal candidate job search | StudentAuth / CandidateAuth |
| **Candidate** | `GET` | `/api/v1/students/recommendations` | Dynamically scored reverse-matching feed | StudentAuth / CandidateAuth |
| **Candidate** | `GET` | `/api/v1/students/skill-gap-roadmap` | High-priority upskilling skills & deliverables | StudentAuth / CandidateAuth |
| **Candidate** | `POST` | `/api/v1/students/jobs/{id}/apply` | 1-click ACID application submission | StudentAuth / CandidateAuth |
| **Candidate** | `GET` | `/api/v1/students/applications` | Student application pipeline & stage history | StudentAuth / CandidateAuth |
| **Internship** | `GET` | `/api/v1/students/internships/active` | Student live ongoing internship tracker & mentor reviews | StudentAuth / CandidateAuth |
| **Internship** | `POST` | `/api/v1/students/internships/{id}/log-milestone` | Student logs weekly milestone, deliverables & hours | StudentAuth / CandidateAuth |
| **Candidate** | `GET` | `/api/v1/students/notifications` | Real-time notifications & opportunity alerts | StudentAuth / CandidateAuth |
| **Candidate** | `GET` | `/api/v1/students/deadlines` | Approaching position deadlines | StudentAuth / CandidateAuth |
| **Candidate** | `POST` | `/api/v1/students/deadlines/check-reminders` | 72-hour deadline reminder scanner | StudentAuth / CandidateAuth |
| **Recruiter** | `GET` | `/api/v1/recruiters/me` | Recruiter profile & company details | RecruiterAuth |
| **Recruiter** | `PUT` | `/api/v1/recruiters/me` | Update recruiter designation & department | RecruiterAuth |
| **Recruiter** | `POST` | `/api/v1/recruiters/company` | Register or update company branding & CIN | RecruiterAuth |
| **Recruiter** | `POST` | `/api/v1/listings/` | Create & publish new job, internship or FDP listing | RecruiterAuth |
| **Recruiter** | `GET` | `/api/v1/listings/my-listings` | Company job postings across all lifecycle states | RecruiterAuth |
| **Recruiter** | `GET` | `/api/v1/students/search` | 3-signal candidate talent search (`blind=true` support) | RecruiterAuth |
| **Recruiter** | `GET` | `/api/v1/listings/{id}/applicants` | Review applicants (`blind=true` toggle support) | RecruiterAuth |
| **Recruiter** | `PATCH`| `/api/v1/applications/{id}/status` | ACID stage transition with `select_for_update` | RecruiterAuth |
| **Supervision**| `PATCH`| `/api/v1/applications/{id}/internship-progress` | Mentor qualitative feedback, 1-5 rating & certificate issuance | RecruiterAuth |
| **Programs** | `GET` | `/api/v1/programs/` | Corporate learning programs, workshops & challenges feed | Public / JWTAuth |
| **Programs** | `POST` | `/api/v1/programs/` | Publish new training program, workshop, or challenge | RecruiterAuth |
| **Programs** | `GET` | `/api/v1/programs/{id}` | Detailed syllabus, dates, and learning outcomes | Public / JWTAuth |
| **Programs** | `POST` | `/api/v1/programs/{id}/enroll` | 1-click enrollment for students and faculty | JWTAuth |
| **Academia** | `GET` | `/api/v1/institutions/directory` | Directory of verified colleges & departments | Public |
| **Academia** | `POST` | `/api/v1/institutions/` | Register new college / institution | AcademiaAuth |
| **Academia** | `POST` | `/api/v1/institutions/{id}/departments` | Add academic department | AcademiaAuth |
| **Academia** | `GET` | `/api/v1/institutions/faculty/me` | Faculty profile & institution info | AcademiaAuth |
| **Academia** | `PUT` | `/api/v1/institutions/faculty/me` | Update faculty profile & designation | AcademiaAuth |
| **Faculty Opps**| `GET` | `/api/v1/institutions/faculty/opportunities` | Faculty internships, FDPs, consultancies discovery | AcademiaAuth |
| **Faculty Opps**| `POST`| `/api/v1/institutions/faculty/opportunities/{id}/apply`| Faculty 1-click application for industrial exposure | AcademiaAuth |
| **Faculty Opps**| `GET` | `/api/v1/institutions/faculty/my-collaborations` | Faculty enrolled collaboration tracks & programs | AcademiaAuth |
| **Faculty** | `GET` | `/api/v1/placement/overview` | Idempotent institutional placement metrics | AcademiaAuth |
| **Faculty** | `GET` | `/api/v1/placement/branch-wise` | Branch-wise placement rates & cognitive averages | AcademiaAuth |
| **Faculty** | `GET` | `/api/v1/placement/student-status` | Student offer letters & certification roster | AcademiaAuth |
| **Faculty** | `GET` | `/api/v1/placement/skill-gaps` | Departmental skill deficit radar & syllabus tips | AcademiaAuth |
| **Faculty** | `GET` | `/api/v1/placement/in-demand-skills` | Top industry skills & campus coverage radar | AcademiaAuth |
| **Faculty** | `GET` | `/api/v1/placement/trends` | Pipeline funnel velocities & role breakdown | AcademiaAuth |

---

## ⚡ Database Scalability & Backend Reliability Architecture

To support peak evaluation spikes and prevent database throttling during high-concurrency screening, the backend incorporates 6 production-grade architectural safeguards:

| Pillar | Engineering Safeguard | Implementation Mechanism |
|---|---|---|
| **Vector Search** | **HNSW Vector Indexing** | Native `pgvector` HNSW indexes (`HnswIndex`, `vector_cosine_ops`, $M=16$, $ef=64$) on `StudentProfile.embedding` and `JobListing.embedding` replace sequential scans with sub-millisecond approximate nearest neighbor (ANN) retrieval. |
| **ORM Optimization** | **Zero N+1 Queries** | Multi-level `Prefetch` on candidate offers and annotated `Count(..., distinct=True)` aggregations on program enrollments collapse query loops into single-digit constant queries. |
| **Connection Pooling** | **Persistent TCP & PgBouncer** | `CONN_MAX_AGE = 600` (10-minute TCP socket persistence) and `CONN_HEALTH_CHECKS = True` eliminate connection churn and socket depletion. |
| **Concurrency Safety** | **Transactional Idempotency** | Duplicate `/apply` calls return `200 OK` with the existing record, and `/status` retries return current state without creating redundant audit history or duplicate alerts. |
| **Stateless Auth** | **Zero-DB Role Pre-Check** | `RecruiterAuth`, `StudentAuth`, and `AcademiaAuth` decode JWTs and validate the `role` claim prior to database execution, rejecting unauthorized requests with 0 DB roundtrips. |
| **Resilience** | **Graceful AI Degradation** | Structured fallbacks for resume analysis, 5-question adaptive tests, and viva scoring provide Apple-grade polite system messaging if external AI models experience network latency. |

---

## 🛡️ Anti-Cheat & Plagiarism Protections Summary

| Vector | Protection Layer | Implementation Mechanism |
|---|---|---|
| **External Search Hesitation** | Linear Time Decay ($M_t$) | `time_taken_seconds` measured client-side; penalties trigger beyond 15s |
| **Copied Answer Detection** | Keystroke Velocity Delta | Instantaneous long text entry flags a warning in system audit logs |
| **Inspect Element / Network Tampering** | Server-Side Rubrics | Correct answers and scoring anchors are withheld entirely from API responses |
| **Resume Padding / Exaggeration** | Non-Linear $CS$ Penalty | Abnormally high gaps between resume claims and assessment scores penalize profile confidence |
| **Database Row Contention** | ACID `select_for_update` | Atomically locks rows during stage advancement; returns HTTP 409 Conflict upon race conditions |

---

<img width="1919" height="987" alt="image" src="https://github.com/user-attachments/assets/5d0a653d-de0e-4bc7-9bf1-f2ab4894e0d4" />


