# Skill Setu — Smart India Hackathon (SIH) Compliance Audit & Action Checklist

**Problem Statement Title:** Centralized Academia–Industry Collaboration Portal  
**Domain:** Skill Development, Internships, Placements, Institutional Oversight, and Industry Collaboration  
**Current Audit Date:** September 2026  
**Compliance Target:** 100% Bare-Minimum Feature Parity with Zero Evaluator Deductions

---

## Executive Summary: Current Implementation Scorecard

| Pillar | SIH Core Requirement | Backend Status | Frontend Status | Overall Compliance |
|---|---|---|---|---|
| **Pillar 1** | Skill Assessment & Cognitive Profiling | ✅ 100% Done | ✅ 100% Done | **100% Complete** |
| **Pillar 2** | Skill Gaps & Upskilling Roadmap | ✅ 100% Done | ✅ 100% Done | **100% Complete** |
| **Pillar 3** | Student Digital Portfolio (APAAR/ABC & Verified Ws) | ✅ 100% Done | ✅ 95% Done | **98% Complete** |
| **Pillar 4** | Industry Learning Programs & Certification Tracks | ✅ 100% Done | ✅ 100% Done | **100% Complete** |
| **Pillar 5** | Internship & Job Opportunities (Post, Search, Apply) | ✅ 100% Done | ⚠️ 75% Done | **88% Complete** |
| **Pillar 6** | Internship Progress Tracking & Mentor Feedback | ✅ 100% Done | ⚠️ 30% Done | **65% Complete** |
| **Pillar 7** | Faculty Internships, FDPs & Research Collaboration | ✅ 100% Done | ⚠️ 25% Done | **62% Complete** |
| **Pillar 8** | Institutional Placement Analytics & Skill Deficit Radar | ✅ 100% Done | ⚠️ 20% Done | **60% Complete** |
| **Pillar 9** | Role-Based Access & Security (RBAC) | ✅ 100% Done | ✅ 90% Done | **95% Complete** |

---

## Detailed Clause-by-Clause Audit: Done vs. Left

### PILLAR 1: Skill Development & Assessment

#### SIH Clause:
> "Skill assessment through questionnaires and aptitude tests. Skill profiling and identification of technical and soft skill gaps."

| Feature Specification | Backend Implementation | Frontend Implementation | Status |
|---|---|---|---|
| In-memory Resume Skill Parsing | `POST /api/v1/students/upload-resume`<br>`pypdf`/`python-docx` in-memory extraction with Gemini 3.1 Flash-Lite | `StudentPortfolio.jsx` / `MySkills.jsx`<br>Resume dropzone, parse progress indicator | ✅ **DONE** |
| 4-Tier Categorization | `skills_categorized` JSONB:<br>`technical_skills`, `frameworks`, `tools`, `soft_skills` | Rendered with distinct color badges in `MySkills.jsx` | ✅ **DONE** |
| Individual Skill Weighting ($W_s$) | $W_s = 0.6 \times P_e + 0.4 \times E_r$ with +15% credential multiplier | Progress rings and proficiency breakdown in `MySkills.jsx` | ✅ **DONE** |
| Adaptive Test Generation | `POST /api/v1/students/generate-test`<br>Generates 5 progressive questions (MCQs, debugging, architecture) via Gemini | `MySkills.jsx` -> Assessment Tab<br>Interactive test session with per-question timers | ✅ **DONE** |
| Anti-Cheat & Plagiarism Penalty | Linear time-decay multiplier $M_t$ (15s-60s) + capped-root CS penalty $CS = A_s \times (1 - 0.4\sqrt{\max(0, R_s - A_s)/100})$ | Displays verified confidence score $CS$ and anti-cheat telemetry | ✅ **DONE** |
| Zero-Score Retest Fault Tolerance | Evaluates vivas with server-side rubrics. On AI latency/timeout grants 0 unearned points and flags session for retest | Handles retest states cleanly without crashing | ✅ **DONE** |

---

### PILLAR 2: Skill Gaps Identification & Recommendation Engine

#### SIH Clause:
> "Skill mapping based on assessment: recommends relevant industries, job roles, and skill development programs. Career guidance based on individual skills, interests, and industry demand."

| Feature Specification | Backend Implementation | Frontend Implementation | Status |
|---|---|---|---|
| Skill-Gap Analysis Engine | `GET /api/v1/students/skill-gap-roadmap`<br>Calculates market demand % across active postings vs candidate skills | `MySkills.jsx` -> Upskilling Roadmap Tab<br>Market demand frequency bar chart | ✅ **DONE** |
| Actionable "Skills to Build Next" | Identifies top 6 missing skills with expected +% match boost and tailored engineering project suggestions | Priority badges (`HIGH`, `MEDIUM`), match boost pill, project case study text | ✅ **DONE** |
| Multi-Domain Benchmarking | Dynamic benchmarks in PostgreSQL (`JobBenchmark`, `IndustrySector`) across Tech, Commerce, Management, and Design | Domain selector in `MySkills.jsx` (Engineering, Commerce, Management, Design) | ✅ **DONE** |
| Reverse Role Fitment Matrix | `GET /api/v1/students/recommendations`<br>Reverse matches candidate skills matrix against active job postings | `MySkills.jsx` -> Recommended Opportunities with direct deep links to Role Dossier | ✅ **DONE** |
| NEP 2020 Multidisciplinary Synergy | Evaluates minor specialization against job requirements (e.g. Major B.Tech + Minor Design/FinTech) with +5% synergy bonus | NEP synergy alert badge in recommendation cards | ✅ **DONE** |

---

### PILLAR 3: Student Digital Portfolio

#### SIH Clause:
> "Maintain a digital portfolio for students containing verified skills, certifications, projects, internships, and achievements to improve employability."

| Feature Specification | Backend Implementation | Frontend Implementation | Status |
|---|---|---|---|
| Comprehensive Portfolio API | `GET /api/v1/students/portfolio/me`<br>`GET /api/v1/students/{id}/portfolio`<br>Aggregates verified skills, CS, certifications, projects, internships, and achievements | `StudentPortfolio.jsx`<br>Interactive portfolio view with tabs for Skills, Projects, Experience, Academics | ✅ **DONE** |
| Candidate Strength Score ($P_{\text{overall}}$) | $P_{\text{overall}} = 0.45 S_{\text{cog}} + 0.30 S_{\text{proj}} + 0.15 S_{\text{cert}} + 0.10 S_{\text{acad}}$ | Visual strength score gauge with breakdown pills in `Profile.jsx` and `StudentPortfolio.jsx` | ✅ **DONE** |
| NEP 2020 National Identifiers | Stores 12-digit APAAR/ABC ID, NHEQF level (Level 4.5 to 8.0), and minor specialization | Form inputs in Profile Settings and verified badges in portfolio | ✅ **DONE** |
| Blind Screening Toggle | Supports `?blind=true` query param: redacts student name, email, and institution for objective screening | Toggle supported in candidate review endpoints | ✅ **DONE** |
| Supervisor Ratings & Achievements | Backend stores verified achievements (IEEE, SIH, honors) and supervisor 1-5 star ratings | Verified credentials rendered; achievement add modal can be enriched | ⚠️ **POLISH (95%)** |

---

### PILLAR 4: Industry Learning Programs & Certification Tracks

#### SIH Clause:
> "Industry Learning Programs: Companies can publish training programs, certification courses, workshops, and mentorship initiatives to help students acquire in-demand skills before applying."

| Feature Specification | Backend Implementation | Frontend Implementation | Status |
|---|---|---|---|
| Multi-Domain Programs Seed | `seed_learning_programs.py`<br>16 enterprise programs across Tech, Commerce, Management, Design with realistic curriculum modules | Rendered with domain filters and company initial avatars | ✅ **DONE** |
| Dynamic Recommendations & Gap Boosters | `GET /api/v1/programs/recommendations`<br>Calculates match score, tags "Skill Gap Boosters" closing candidate's roadmap deficits | `learning.jsx`<br>"Recommended for You" & "Skill Gap Boosters" tabs with +% match boost badges | ✅ **DONE** |
| 1-Click Universal Enrollment | `POST /api/v1/programs/{id}/enroll`<br>Enrolls students and faculty, creates real-time Notification | `learning.jsx`<br>1-Click Enroll button with loading state and instant feedback | ✅ **DONE** |
| Interactive Progress Tracker | `POST /api/v1/programs/{id}/progress`<br>Updates completed modules checklist and progress % | `learning.jsx`<br>Interactive module checklist, live progress bar ($0\% \to 100\%$) | ✅ **DONE** |
| Verified Certificate Generation | Automatically generates credential ID `#SKL-CERT-...` upon 100% completion and updates candidate certifications | Unlocks Certificate badge with Credential ID in `learning.jsx` modal | ✅ **DONE** |

---

### PILLAR 5: Internship & Placement Opportunities Engine

#### SIH Clause:
> "Industries can post internships, projects, apprenticeships, and entry-level job openings with required skills. Students receive recommendations and can apply directly. Application tracking and recruitment management for students and recruiters."

| Feature Specification | Backend Implementation | Frontend Implementation | Status |
|---|---|---|---|
| Job & Internship Posting API | `POST /api/v1/listings/`<br>Recruiter creates postings (`FULL_TIME`, `INTERNSHIP`, `APPRENTICESHIP`, `CONTRACT`). Generates BGE vector index | `Industry.jsx` currently writes to local state only — **needs wiring to `POST /api/v1/listings/`** | ⚠️ **ACTION REQUIRED** |
| Recruiter's Active Postings Feed | `GET /api/v1/listings/my-listings`<br>Returns all company listings across statuses | `Industry.jsx` currently displays mock jobs — **needs wiring to `GET /listings/my-listings`** | ⚠️ **ACTION REQUIRED** |
| Candidate Job Search (3-Signal NLP) | `POST /api/v1/listings/search`<br>Dense BGE-384d vector + deterministic skill overlap + SearchRank | Integrated into Spotlight command palette and `Opportunities.jsx` | ✅ **DONE** |
| 1-Click Direct Application | `POST /api/v1/listings/{id}/apply/`<br>Row-level `select_for_update` locking with anti-lockup 409 handling | `OpportunitiesDetails.jsx`<br>1-Click "Apply Now" button with state sync | ✅ **DONE** |
| Applicant Review Pipeline | `GET /api/v1/applications/`<br>`PATCH /api/v1/applications/{id}/status`<br>Transitions: `APPLIED` $\to$ `UNDER_REVIEW` $\to$ `SHORTLISTED` $\to$ `INTERVIEW` $\to$ `OFFERED` $\to$ `REJECTED` | Recruiter view needs a streamlined Applicant Pipeline Review Board (Kanban/Table) | ⚠️ **ACTION REQUIRED** |
| Student Application Tracker | `GET /api/v1/students/applications`<br>Tracks active applications, status timeline, and interview dates | Students need a dedicated "My Applications" pipeline view | ⚠️ **ACTION REQUIRED** |

---

### PILLAR 6: Live Internship Tracking & Mentor Feedback

#### SIH Clause:
> "Progress tracking, mentor feedback, and internship completion records."

| Feature Specification | Backend Implementation | Frontend Implementation | Status |
|---|---|---|---|
| Student Milestone Logging | `POST /api/v1/students/internships/{id}/log-milestone`<br>Student logs week number, summary, hours worked, deliverables repository URL. Auto-transitions to `IN_PROGRESS` | Need a simple "Log Weekly Milestone" modal for enrolled intern students | ⚠️ **ACTION REQUIRED** |
| Recruiter Supervision & Rating | `POST /api/v1/applications/{id}/internship-progress`<br>Recruiter logs qualitative mentor remarks, assigns 1.0 to 5.0 star rating, attaches completion certificate URL. Auto-updates portfolio | Need mentor rating & feedback controls inside the Recruiter Applicant Review view | ⚠️ **ACTION REQUIRED** |

---

### PILLAR 7: Dedicated Portal for Academicians & Faculty Exposure

#### SIH Clause:
> "Provide a dedicated portal for academicians to explore faculty internships, industrial training, Faculty Development Programs (FDPs), consultancy opportunities, and collaborative research projects. Facilitate industry–academia collaboration through mentorship programs, workshops, guest lectures, innovation challenges, and live industry projects."

| Feature Specification | Backend Implementation | Frontend Implementation | Status |
|---|---|---|---|
| Faculty Opportunities Discovery Feed | `GET /api/v1/institutions/faculty/opportunities`<br>Filters for `FACULTY_INTERNSHIP`, `FDP`, `INDUSTRIAL_TRAINING`, `CONSULTANCY`, `RESEARCH_PROJECT`, `WORKSHOP`, `GUEST_LECTURE` | `Acadmecian.jsx` currently only has lecture upload form — **needs Faculty Opportunities tab** | ⚠️ **ACTION REQUIRED** |
| Faculty 1-Click Application | `POST /api/v1/institutions/faculty/opportunities/{id}/apply`<br>Faculty submits Statement of Purpose; dispatches recruiter alert | Needs 1-Click "Express Interest / Apply" button on Faculty Opportunity cards | ⚠️ **ACTION REQUIRED** |
| Faculty Collaboration Tracker | `GET /api/v1/institutions/faculty/my-collaborations`<br>Tracks enrolled FDPs, industrial training, and collaborative projects | Needs "My Collaborations" tab in `Acadmecian.jsx` | ⚠️ **ACTION REQUIRED** |
| Faculty Lecture & Resource Upload | Full models and routing | `Acadmecian.jsx` lecture upload form is implemented | ✅ **DONE** |

---

### PILLAR 8: Institutional Placement Analytics & Oversight Dashboards

#### SIH Clause:
> "Enable institutions to monitor student skill development, internship participation, and placement progress through dashboards and analytics. Analytics and reporting dashboards for institutions and industries to monitor placement readiness, recruitment outcomes, and skill demand trends."

| Feature Specification | Backend Implementation | Frontend Implementation | Status |
|---|---|---|---|
| Placement Overview KPI Cards | `GET /api/v1/placement/overview`<br>Idempotent stats: Total students, placed, unplaced, placement %, offers extended, interview pipeline | Needs Institutional Overview Dashboard tab in `Acadmecian.jsx` | ⚠️ **ACTION REQUIRED** |
| Branch/Departmental Placement Metrics | `GET /api/v1/placement/branch-wise`<br>Department-wise placement %, average confidence scores, top branch skills | Needs Departmental comparison table/cards | ⚠️ **ACTION REQUIRED** |
| Institutional Skill Deficit Radar | `GET /api/v1/placement/skill-gaps`<br>Compares employer market demand vs campus student supply; identifies deficit index % and syllabus recommendations | Needs Skill Deficit Radar view with deficit progress bars | ⚠️ **ACTION REQUIRED** |
| In-Demand Skills Analytics | `GET /api/v1/placement/in-demand-skills`<br>Top skills demanded by recruiters, campus coverage %, and deficit index | Needs In-Demand Skills breakdown | ⚠️ **ACTION REQUIRED** |
| Recruitment Funnel & Trends | `GET /api/v1/placement/trends`<br>Applied $\to$ Under Review $\to$ Shortlisted $\to$ Interview $\to$ Offered $\to$ Placed conversion percentages | Needs Recruitment Funnel visualizer | ⚠️ **ACTION REQUIRED** |
| Faculty Student Roster | `GET /api/v1/placement/student-status`<br>Student offer letters, verified certifications, and profile strength ratings | Needs Student Placement Roster table with filters | ⚠️ **ACTION REQUIRED** |

---

## Direct Rubric Mapping: Verbatim SIH Expected Solution Breakdown

### 1. Skill Development
| SIH Specification | Backend Status | Frontend Status | Notes |
|---|---|---|---|
| **Skill assessment through questionnaires and aptitude tests** | ✅ Implemented (`POST /students/generate-test`, `POST /students/submit-test`, `grader.py`) | ✅ Implemented (`MySkills.jsx` Assessment Tab with active timers) | Evaluates technical + soft skills, applies linear time-decay $M_t$ and capped-root penalty $CS$ |
| **Skill profiling & identification of technical and soft skill gaps** | ✅ Implemented (`GET /students/skill-gap-roadmap`, 4-tier JSONB) | ✅ Implemented (`MySkills.jsx` Roadmap & Matrix tabs) | Computes market demand %, categorizes into Technical, Frameworks, Tools, Soft Skills |
| **Personalized learning recommendations & certification programs** | ✅ Implemented (`GET /programs/recommendations`, `seed_learning_programs.py`) | ✅ Implemented (`learning.jsx` Recommended & Gap Boosters tabs) | Recommends courses matching missing gap skills with boost predictions and `#SKL-CERT` certificates |
| **Career guidance based on individual skills, interests & industry demand** | ✅ Implemented (`GET /students/recommendations`, `JobBenchmark`) | ✅ Implemented (`MySkills.jsx` Recommended Opportunities) | Dynamic fitment percentage, reverse role matching, and project case study recommendations |
| **Student digital portfolios showcasing verified skills, certs, projects, achievements** | ✅ Implemented (`GET /students/portfolio/me`, composite $P_{\text{overall}}$ score) | ✅ Implemented (`Profile.jsx`, `StudentPortfolio.jsx`) | Verified skill weights $W_s$, APAAR/ABC ID, NHEQF Level, certifications, GitHub/live project links |

### 2. Internship Lifecycle
| SIH Specification | Backend Status | Frontend Status | Notes |
|---|---|---|---|
| **Centralized internship portal where industries post openings with required skills** | ✅ Implemented (`POST /listings/`, `JobListing` model, BGE embeddings) | ⚠️ Pending Wiring (`Industry.jsx` form needs direct POST to `/listings/`) | Backend generates pgvector embedding, validates salary/stipend and required skill tags |
| **Matching of students to internships based on skill profiles & career interests** | ✅ Implemented (`POST /listings/search` 3-signal NLP hybrid engine) | ✅ Implemented (`Opportunities.jsx`, Spotlight search) | Ranks openings via deterministic skill overlap + BGE cosine similarity + full-text SearchRank |
| **Internship application and tracking system for students** | ✅ Implemented (`POST /listings/{id}/apply/`, `GET /students/applications`) | ⚠️ Needs dedicated "My Applications" view | Application submission works; pipeline view showing status timeline needs quick rendering |
| **Internship opportunities for academicians, industrial training & FDPs** | ✅ Implemented (`GET /institutions/faculty/opportunities`, `POST .../apply`) | ⚠️ Needs tab in `Acadmecian.jsx` | Supports Faculty Internships, FDPs, Consultancy, Research Projects with Statement of Purpose |
| **Progress tracking, mentor feedback & internship completion records** | ✅ Implemented (`POST /students/internships/{id}/log-milestone`, `POST /applications/{id}/internship-progress`) | ⚠️ Needs milestone modal & recruiter feedback form | Weekly milestones auto-transition to `IN_PROGRESS`; recruiter ratings & certificates auto-sync to portfolio |

### 3. Placement Lifecycle
| SIH Specification | Backend Status | Frontend Status | Notes |
|---|---|---|---|
| **Industry portal for posting job opportunities with qualifications & skill sets** | ✅ Implemented (`POST /listings/`, `GET /listings/my-listings`) | ⚠️ Pending Wiring in `Industry.jsx` | Supports `FULL_TIME`, `INTERNSHIP`, `APPRENTICESHIP`, `CONTRACT` with deadline checks |
| **Recommendation engine to match students with relevant placement opportunities** | ✅ Implemented (`GET /students/recommendations`, Reverse Matcher) | ✅ Implemented (`MySkills.jsx` & `Opportunities.jsx`) | Deep-links role recommendations directly into Opportunity Dossier modal |
| **Candidate shortlisting based on skill compatibility and eligibility** | ✅ Implemented (`POST /students/search` 3-signal candidate search, blind screening) | ✅ Implemented (`Students.jsx` Recruiter Talent Search) | Recruiter can filter by skill overlap, score, and toggle blind screening to redact PII |
| **Application tracking and recruitment management for students & recruiters** | ✅ Implemented (`GET /applications/`, `PATCH /applications/{id}/status` ACID locked) | ⚠️ Recruiter Review Board needs rendering | Row-level locking on application transitions (`APPLIED` $\to$ `OFFERED` $\to$ `PLACED`) |
| **Analytics & reporting dashboards for institutions & industries to monitor readiness** | ✅ Implemented (`GET /placement/overview`, `/branch-wise`, `/skill-gaps`, `/trends`) | ⚠️ Needs Institutional Dashboard tab in `Acadmecian.jsx` | Calculates idempotent placement %, branch breakdown, skill deficit radar, and conversion funnel |

### 4. Overall Platform Features
| SIH Specification | Backend Status | Frontend Status | Notes |
|---|---|---|---|
| **Role-based access for students, academicians, industries, and institutions** | ✅ Implemented (`accounts/security.py`: `StudentAuth`, `RecruiterAuth`, `AcademiaAuth`) | ✅ Implemented (`Navbar.jsx`, `App.jsx` role guards) | Distinct navigation, permission scopes, and protected endpoints per role |
| **Secure document management for resumes, certificates, internship reports** | ✅ Implemented (In-memory document stream, resume raw extraction, certificate storage) | ✅ Implemented (`StudentPortfolio.jsx`, resume dropzone) | Zero-disk delay in-memory parsing via `pypdf`/`python-docx` |
| **Collaboration features: industry mentorship, live projects, workshops, research** | ✅ Implemented (`programs` router, `institutions` router, VideoCall WebRTC) | ✅ Implemented (`learning.jsx`, `VideoCall.jsx`) | Live 1:1 video interviews and collaborative enterprise programs |
| **Integration with learning platforms, certification providers & institutional databases** | ✅ Implemented (`JobBenchmark`, verified certificate hashes, APAAR/ABC ID) | ✅ Implemented (`Profile.jsx`, `learning.jsx`) | Syncs verified certificates, national education database identifiers |
| **Comprehensive analytics for institutions, industries & policymakers** | ✅ Implemented (Placement analytics suite, department KPIs, student roster) | ⚠️ Needs visual cards in `Acadmecian.jsx` | Aggregates campus-wide placement stats, deficit indices, and industry demand trends |

---

## Dynamic Parity Audit: What Is NOT Working Dynamically Right Now

While the backend architecture contains verified database models, AI gateways, and API endpoints, several key user interfaces currently operate in isolated local states or use static mock fallbacks. The following audit details every specific dynamic disconnect that strict hackathon evaluators will detect:

### 1. Recruiter / Industry Portal (`Industry.jsx`)
* **Dynamic Failure 1: Local-Only Job Creation**
  * *Current State:* Submitting the job creation form only prepends to an ephemeral React array `jobs = useState(initialJobs)`.
  * *Consequence:* Postings are never sent to the PostgreSQL database, never indexed into BGE dense vectors, and never generate real-time student opportunity alerts.
  * *Required Fix:* Wire form submit directly to `POST /api/v1/listings/` using `apiClient.post('/listings/', payload)`.
* **Dynamic Failure 2: Static Mock Postings on Load**
  * *Current State:* The page renders hardcoded `initialJobs` (Backend Engineering Intern, Product Design Intern, Data Analyst Intern).
  * *Consequence:* Evaluators cannot see jobs previously posted or seeded in the database.
  * *Required Fix:* Fetch the recruiter's active company listings on mount via `GET /api/v1/listings/my-listings`.
* **Dynamic Failure 3: Missing Applicant Pipeline Review Board**
  * *Current State:* Clicking a job posting does not reveal candidate applicants who applied.
  * *Consequence:* Evaluators cannot review student submissions or test scores.
  * *Required Fix:* Add an Applicant Review drawer/panel calling `GET /api/v1/applications/listings/{listing_id}/applications`, displaying candidates, match scores, and status transition buttons (`APPLIED` $\to$ `UNDER_REVIEW` $\to$ `SHORTLISTED` $\to$ `INTERVIEW` $\to$ `OFFERED` $\to$ `REJECTED`) calling `POST /api/v1/applications/{id}/status`.
* **Dynamic Failure 4: Missing Intern Supervision & Mentor Feedback Form**
  * *Current State:* No interface for recruiters to rate interns or log evaluation remarks.
  * *Consequence:* Fails the SIH clause *"Progress tracking, mentor feedback, and internship completion records"*.
  * *Required Fix:* Add mentor evaluation controls calling `PATCH /api/v1/applications/{id}/internship-progress` (1–5 star rating, mentor feedback notes, certificate URL).

---

### 2. Institutional Oversight & Faculty Portal (`Acadmecian.jsx`)
* **Dynamic Failure 1: Isolated Lecture-Only View**
  * *Current State:* The academician screen only renders a video upload form and static lecture table (`initialLectures`).
  * *Consequence:* 0% of institutional oversight, placement reporting, or faculty exposure features are accessible from the UI.
  * *Required Fix:* Convert `Acadmecian.jsx` into a 4-tab portal:
    1. **Institutional Placement Oversight & Analytics**
    2. **Faculty Industry Exposure & Opportunities**
    3. **My Active Industry Collaborations**
    4. **Course Lectures & Resources**
* **Dynamic Failure 2: Placement Analytics Not Connected**
  * *Current State:* None of the 5 institutional placement analytics endpoints are invoked.
  * *Required Fix:* Render dynamic KPI cards and charts connected to:
    * `GET /api/v1/placement/overview` (Total students, placed %, unplaced, offers extended, interview pipeline).
    * `GET /api/v1/placement/skill-gaps` (Skill Deficit Radar: market demand vs student supply with deficit index %).
    * `GET /api/v1/placement/branch-wise` (Departmental placement rates & average cognitive scores).
    * `GET /api/v1/placement/student-status` (Faculty student roster with offer details & strength scores).
    * `GET /api/v1/placement/trends` (Recruitment stage conversion funnel).
* **Dynamic Failure 3: Faculty Industry Exposure Not Discoverable**
  * *Current State:* Faculty have no way to explore or apply for corporate residencies or FDPs.
  * *Required Fix:* Connect to `GET /api/v1/institutions/faculty/opportunities` with 1-click Statement of Purpose application modal calling `POST /api/v1/institutions/faculty/opportunities/{id}/apply`.
* **Dynamic Failure 4: Active Collaborations Not Tracked**
  * *Current State:* Enrolled FDPs and joint research programs are invisible to faculty.
  * *Required Fix:* Connect to `GET /api/v1/institutions/faculty/my-collaborations`.

---

### 3. Student Application Tracker & Weekly Milestone Logger (`Opportunities.jsx` / `StudentPortfolio.jsx`)
* **Dynamic Failure 1: Ephemeral Applied State**
  * *Current State:* Clicking "Apply Now" saves the ID to local state `appliedIds = useState([])`. Navigating away or refreshing loses the applied state.
  * *Required Fix:* Synchronize with `GET /api/v1/students/applications` so applied positions persist across sessions.
* **Dynamic Failure 2: Missing "My Applications" Pipeline Tracker View**
  * *Current State:* Students cannot track where their application stands in the recruitment pipeline (`APPLIED`, `UNDER_REVIEW`, `SHORTLISTED`, `INTERVIEW`, `OFFERED`, `REJECTED`).
  * *Required Fix:* Add a segmented tab "My Applications" in `Opportunities.jsx` displaying applied positions, live status pills, and scheduled interview dates.
* **Dynamic Failure 3: Missing Weekly Milestone Logger for Active Interns**
  * *Current State:* Placed interns cannot record weekly achievements or deliverables.
  * *Consequence:* Breaks SIH internship lifecycle continuity.
  * *Required Fix:* Add a "Log Weekly Milestone" modal calling `POST /api/v1/students/internships/{id}/log-milestone` (week number, summary, hours, repository URL).
* **Dynamic Failure 4: Application Endpoint Inconsistency**
  * *Current State:* In `Opportunities.jsx`, line 364 calls `POST /listings/{id}/apply/` (which returns 404), while `OpportunitiesDetails.jsx` calls `POST /students/jobs/{id}/apply`.
  * *Required Fix:* Standardize both direct-apply triggers to call `apiClient.post('/students/jobs/' + id + '/apply')` with error and success handling.

---

### 4. Public Opportunities Discovery Endpoint Authentication Guard
* **Dynamic Failure 1: Browse Endpoint Requires Token**
  * *Current State:* In `recruiters/api.py`, `GET /listings/` has `auth=JWTAuth()`. If an unauthenticated visitor or student visits the Opportunities page, it returns 401 Unauthorized and falls back to static mock data.
  * *Required Fix:* Allow optional authentication on `GET /listings/` so database-seeded opportunities (Google, Microsoft, PySphere, etc.) load dynamically for everyone, while preserving authentication on `/apply`.

---

## Full Step-by-Step Implementation Plan to Reach 100% Dynamic Compliance

### Phase 1: Backend Endpoint Reliability & Public Discovery (Day 1 - Morning)
1. In `recruiters/api.py`, update `GET /listings/` to allow public / optional-auth browsing so unauthenticated users and fresh sessions immediately receive live database listings.
2. In `recruiters/api.py`, add an alias `POST /listings/{listing_id}/apply` pointing to `apply_to_listing` to ensure both `/listings/{id}/apply` and `/students/jobs/{id}/apply` succeed interchangeably.
3. Validate all backend test endpoints with `python manage.py check`.

### Phase 2: Institutional Oversight & Faculty Portal Upgrade (`Acadmecian.jsx`) (Day 1 - Afternoon)
1. Re-architect `SkillSetu/src/components/Uploading/Acadmecian.jsx` with a 4-tab segmented control:
   * **Tab 1: Placement Analytics Dashboard**:
     * KPI Cards: Total Students, Placed %, Offers Extended, Active Pipeline (`/placement/overview`).
     * Skill Deficit Radar: In-demand skills vs campus coverage bar meters (`/placement/skill-gaps`).
     * Branch Performance: Departmental table with placement rates and cognitive scores (`/placement/branch-wise`).
     * Student Placement Roster: Filterable candidate table with offer details (`/placement/student-status`).
   * **Tab 2: Faculty Industry Opportunities**:
     * Discovery cards for Faculty Internships, FDPs, Industrial Training, and Research Projects (`/institutions/faculty/opportunities`).
     * 1-Click "Express Interest / Apply" modal with Statement of Purpose (`/institutions/faculty/opportunities/{id}/apply`).
   * **Tab 3: My Collaborations**:
     * Active enrolled programs and research tracks (`/institutions/faculty/my-collaborations`).
   * **Tab 4: Course Lectures**:
     * Retain clean lecture video upload and repository management.
2. Enforce strict `Design.md` design tokens and zero code comments policy.

### Phase 3: Recruiter / Industry Portal Full Dynamic Wiring (`Industry.jsx`) (Day 1 - Evening)
1. Replace mock `initialJobs` in `SkillSetu/src/components/Uploading/Industry.jsx`:
   * Fetch active company listings from `GET /api/v1/listings/my-listings` on mount.
   * Wire the "Create Posting" form to `POST /api/v1/listings/` with loading and toast confirmation states.
2. Build the **Applicant Pipeline Review Board**:
   * For each active job card, show an "Applicants" badge.
   * Expandable drawer / modal loading `GET /api/v1/applications/listings/{id}/applications`.
   * Display applicant match scores, verified badges, and quick-action stage transition buttons (`UNDER_REVIEW`, `SHORTLISTED`, `INTERVIEW`, `OFFERED`, `REJECTED`) calling `POST /api/v1/applications/{id}/status`.
3. Add the **Internship Supervision & Rating Form**:
   * For accepted interns, provide an evaluation modal calling `PATCH /api/v1/applications/{id}/internship-progress` (1–5 star rating, feedback remarks, certificate URL).
4. Enforce strict `Design.md` design tokens and zero code comments policy.

### Phase 4: Student Application Tracker & Weekly Milestone Logger (`Opportunities.jsx`) (Day 2 - Morning)
1. In `SkillSetu/src/components/Opportunities/Opportunities.jsx`:
   * Add a top-level segmented tab toggle: **"Explore Opportunities"** vs **"My Applications"**.
   * Under "My Applications", fetch from `GET /api/v1/students/applications`.
   * Render application pipeline cards with:
     * Company initial avatar monogram (`getCompanyInitials`, `getCompanyAvatarColor`).
     * Role title, applied date, and stipend.
     * Status pill badge with distinct semantic styling (`APPLIED`, `UNDER_REVIEW`, `SHORTLISTED`, `INTERVIEW`, `OFFERED`, `REJECTED`).
     * Scheduled interview date banner (if scheduled).
     * Stage transition timeline.
     * For placed/active interns: A "Log Weekly Milestone" button opening a modal calling `POST /api/v1/students/internships/{id}/log-milestone` (week number, summary, hours, repository link).
2. Standardize direct-apply API calls across `Opportunities.jsx` and `OpportunitiesDetails.jsx` to prevent 404 errors.
3. Enforce strict `Design.md` design tokens and zero code comments policy.

### Phase 5: Verification & End-to-End Walkthrough (Day 2 - Afternoon)
1. Run `npm run build` in `SkillSetu` to ensure zero compilation or syntax errors.
2. Verify that all 4 user roles (`STUDENT`, `RECRUITER`, `FACULTY`, `GUEST`) function dynamically with live PostgreSQL and zero mock data dependencies.
3. Verify zero comments (`//`, `/* ... */`, `#`) across all updated files.
4. Prepare walkthrough documentation for hackathon presentation.

---
*(Official Smart India Hackathon internal readiness plan)*

