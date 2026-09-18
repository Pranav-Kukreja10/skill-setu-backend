# Skill Setu — Comprehensive Skill Architecture & SIH Defense Dossier

This document consolidates the complete architectural definition of **Skill**, the foundational distinction between **Knowledge vs. Skill**, a feature-by-feature **competitive comparison against Instahyre and HirePro**, statutory alignment with **Indian Government Frameworks (NEP 2020, NCrF, NSQF)**, and **core mathematical formulas** designed specifically for presentation and defense in the **Smart India Hackathon (SIH)**.

---

## 1. Executive Summary & SIH Positioning

### The Problem in Indian Higher Education & Talent Acquisition
1. **The Resume Padding Crisis:** Over 75% of graduate resumes feature inflated keyword claims, unearned certifications, and generative-AI-polished buzzwords. Traditional ATS engines (e.g., Instahyre, Naukri) rely on superficial string matching without verifying capability.
2. **The Assessment Chasm:** Legacy assessment suites (e.g., HirePro) deploy rigid, static question banks and webcam proctoring that induce test fatigue, leak easily online, and fail to measure practical problem-solving.
3. **The Academic-Industry Disconnect:** Universities and Training & Placement Cells (TPOs) operate blind to real-time market demands, resulting in outdated syllabi and unplaced graduates.

### Skill Setu's Closed-Loop Paradigm Shift
Skill Setu replaces honor-system resumes and transactional test portals with an **integrated, mathematically verifiable competency ecosystem**:
* **Proof-Driven:** Evaluates project evidence, active codebase commits, and recency rather than static claims.
* **Cognitive-First:** Uses time-decayed MCQs and dynamic AI vivas with rubric anchors to separate memorized syntax from architectural reasoning.
* **Statutory Compliance:** Natively embeds NEP 2020, NCrF, APAAR/ABC ID, and NHEQF standards.
* **Two-Way Ecosystem:** Bridges candidates, recruiters, and academic institutions in a single closed-loop data pipeline.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE SKILL SETU CYCLE                                 │
│                                                                                        │
│     [Student / Candidate] ────► Real-Time AI Viva + Code Screening ($W_s, CS$)         │
│               │                                      │                                 │
│               ▼                                      ▼                                 │
│     [Digital Portfolio] ◄──── [Verified Competency Score ($P_{overall}$)]              │
│               │                                      │                                 │
│               ▼                                      ▼                                 │
│     [Targeted Jobs & DEI] ◄─── [3-Signal Hybrid NLP Search (Deterministic+Dense+Sparse)]│
│               │                                      │                                 │
│               ▼                                      ▼                                 │
│     [Milestone Internships] ──► [Curriculum Gap Radar for Colleges / TPOs]             │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Competitive Analysis: Skill Setu vs. Instahyre vs. HirePro

### A. Full Tabular Comparison Matrix

| Feature Dimension | **Skill Setu** | **Instahyre ("Instant Hire")** | **HirePro** |
| :--- | :--- | :--- | :--- |
| **Core Paradigm** | **Verified Competency Ecosystem:** Real-time cognitive evaluation, project proof, continuous student portfolio & academic governance. | **Talent Marketplace:** Sourcing active & passive candidates; recruiter CRM & outbound messaging. | **Enterprise Assessment / ATS:** High-volume proctoring, campus drive automation & bulk test distribution. |
| **Primary Target** | Students, Multi-Domain Job Seekers, Academic Institutions (Faculty/TPOs), Recruiters. | Experienced tech professionals, tech startups, corporate sourcing teams. | Enterprise IT services (TCS, Wipro, Infosys), BFSI corporate recruiters, college placement cells. |
| **Skill Verification** | **Automated & Continuous:** Real-time dynamic AI viva + time-decayed MCQs with rubric anchors. | **None:** Relies 100% on self-reported resume claims and candidate declarations. | **Static Test Papers:** Pre-configured MCQ papers, coding compilers, and recorded video interviews. |
| **Anti-Cheat & Fraud Protection** | • **Linear Time-Decay ($M_t$):** Distinguishes instant recall from search hesitation.<br>• **Capped-Root Penalty ($CS$):** Punishes gap between claims and test score.<br>• **Zero-Unearned-Score:** Never awards free points on latency/glitch. | None (Recruiters must manually vet candidates). | • Webcam proctoring & facial detection.<br>• Tab-switch and window-blur tracking.<br>• Code plagiarism checks. |
| **Search & Discovery Engine** | **3-Signal Fusion:**<br>1. Deterministic skill overlap<br>2. Dense BGE 384d pgvector cosine similarity<br>3. Full-text SearchRank. | Proprietary "InstaMatch" (keyword frequency, profile activity, search filters). | Relational database filters (Degree, CGPA cutoff, Graduation Year, Test score bands). |
| **Domain Coverage** | **Universal 4-Tier Coverage:**<br>Tech, Commerce & Accounting (GST, Tally, Auditing), Business Management (BRDs, SWOT), Design (Figma, WCAG). | Heavily skewed to Tech/Software Engineering, Product, and Data. | Primarily IT/Software, General Quantitative Aptitude, and BPO operations. |
| **Institutional Governance** | • Departmental skill-gap radar.<br>• Syllabus deficiency index vs. live employer demand.<br>• Idempotent placement reporting. | ❌ Absent (Zero institutional linkage). | ✅ Bulk drive test scheduling and placement cell candidate registration. |
| **Faculty Pathways** | Dedicated Industry Exposure discovery (FDPs, Faculty Internships, Consultancy, Collaborative Research). | ❌ Absent. | ❌ Limited to test coordinator admin dashboards. |
| **Internship Lifecycle** | **Weekly Milestone Tracking:** Logged deliverables, hours worked, supervisor 1–5★ rating, verified portfolio credentialing. | ❌ Absent (Platform exits after hire). | ❌ Absent (Tracks candidates only until final interview stage). |
| **DEI & Affirmative Action** | Live multi-domain Govt Schemes radar (AICTE Pragati, TechSaksham, Adobe WIT, Tata AA) with automated eligibility matching. | ❌ Basic gender tags or enterprise diversity flags. | ❌ Manual recruiter-configured diversity hiring drives. |
| **Cognitive Bias Prevention** | Native **`blind=True` screening** (auto-redacts Name, Email, College while preserving verified $W_s, CS$). | ❌ Full PII visible to recruiters. | ⚠️ Video proctoring inherently exposes candidate PII and appearance. |
| **Upskilling & Roadmaps** | Dynamic Skill-Gap Radar providing personalized project suggestions and expected role match boost percentages. | ❌ Absent. | ❌ Absent (Candidate receives only pass/fail score). |
| **Concurrency & ACID Locks** | Row-level locking (`select_for_update`) on application pipelines; 409 Conflict anti-deadlock protections. | Standard async web queues. | Enterprise batch queues. |

### B. Detailed Competitive Deep-Dive

#### 1. Why Instahyre Fails at True Competency Evaluation
* Instahyre operates on an **honor system**. It parses strings like *"Python, Kubernetes, Financial Modeling"* and matches them using recruiter preference filters. 
* Candidates quickly learn to **game keywords** using generative AI. Recruiters waste 60–70% of initial screening calls filtering out applicants who have pristine resumes but cannot answer basic architectural questions.
* **Skill Setu Advantage:** In Skill Setu, resume parsing is merely step 1. Claims are immediately cross-referenced with GitHub engineering metrics, project complexity ratings, and validated through our dynamic AI viva engine.

#### 2. Why HirePro Fails at Holistic Candidate Growth & Multi-Domain Reach
* HirePro treats assessment as a **punitive gatekeeper** rather than a development tool. Its question banks are static, heavily leaked on student forums, and focus disproportionately on compiler coding tests or abstract aptitude.
* It offers **zero value to candidates after the test**: no learning roadmaps, no portfolio, and no support for non-tech fields like Commerce (CA/CS/GST) or Design (UI/UX).
* **Skill Setu Advantage:** Skill Setu dynamically synthesizes fresh, progressive questions per candidate, spans all academic disciplines, builds a lasting **Digital Portfolio**, and offers actionable upskilling guidance.

---

## 3. What is a "Skill" According to Our Software?

### A. The Core Conceptual Definition
> **A skill is not a keyword written on a resume — it is a proven, measurable capability to apply knowledge to achieve a specific real-world outcome.**

In our software, a capability only qualifies as a **skill** if it satisfies three components:
1. **A Verb (The Action):** *Auditing, Refactoring, Wireframing, Negotiating, Querying.*
2. **A Medium / Tool (The Instrument):** *Tally Prime, PostgreSQL, Figma, Balance Sheets, Python.*
3. **An Outcome (The Deliverable):** *A balanced ledger, a sub-100ms API, a WCAG-compliant design system.*

Without demonstrable action and an output, a claim is classified merely as **passive knowledge or theory**, not a skill.

---

### B. The 4-Tier Universal Multi-Domain Taxonomy (`skills_categorized`)
Our AI Gateway automatically categorizes candidate competencies into four distinct operational layers across all professional fields:

| Category Tier | Operational Meaning | Cross-Domain Examples |
| :--- | :--- | :--- |
| **1. `technical_skills`** | Core functional, domain-specific execution abilities | **Tech:** Python, Query Optimization, REST APIs<br>**Commerce:** Statutory Auditing, GST Filing, TDS Calculation<br>**Management:** Financial Modeling, Market Sizing, SWOT<br>**Design:** User Research, Wireframing, Design Systems |
| **2. `frameworks`** | Methodologies, architectures, standard practices & regulations | **Tech:** Django, React, Microservices, CI/CD<br>**Commerce:** GAAP, IFRS, Double-Entry Accounting<br>**Management:** Agile/Scrum, Six Sigma, Product Requirement Docs (PRD)<br>**Design:** Design Thinking, Heuristic Evaluation, WCAG 2.1 |
| **3. `tools`** | Software, platforms, utilities, and commercial applications | **Tech:** Docker, Git, Postman, Linux CLI<br>**Commerce:** Tally Prime, QuickBooks, Advanced Excel, SAP ERP<br>**Management:** Salesforce CRM, Tableau, Jira, Power BI<br>**Design:** Figma, Adobe Creative Cloud, Miro, Sketch |
| **4. `soft_skills`** | Interpersonal, leadership, and professional execution behaviors | Cross-Domain: Stakeholder Management, Conflict Resolution, Technical Writing, Negotiation, Cross-Functional Teamwork |

---

### C. The Data Representation in PostgreSQL (`skills_matrix`)
In the database, a skill is never stored as a flat string. It is persisted as a JSONB object with mathematical weights:

```json
"postgresql": {
    "weight": 86,
    "project_evidence": 85,
    "experience_recency": 75,
    "is_certified": true,
    "credential_bonus": 1.15,
    "is_github_verified": true
}
```

* **Data Provenance:** The raw, unedited string parsed from the resume is preserved in `raw_extracted_skills` to guarantee complete auditability.
* **Semantic Embeddings:** Each skill is converted into a **384-dimensional dense vector** via `BGE-small`, enabling conceptual semantic matching in recruiter queries.

---

## 4. Knowledge vs. Skill: The Architectural Separation

A central innovation of Skill Setu is the mathematical and architectural separation of **passive knowledge** from **applied skill**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        KNOWLEDGE VS. SKILL: PLATFORM ARCHITECTURE                      │
│                                                                                        │
│   Dimension                 Knowledge Layer                 Skill Layer                │
│   ─────────                 ───────────────                 ───────────                │
│   • Definition              "Knowing What" (Passive)        "Knowing How" (Active)     │
│   • Candidate Input         Degrees, CGPA, Certifications   Projects, Work Experience  │
│   • Codebase Validation     Stored in profile metadata      GitHub commits, CI/CD, PRs │
│   • Cognitive Test          Time-Decayed MCQs (30% weight)  AI Viva Scenarios (70%)    │
│   • Profile Weight ($P_{overall}$) 25% Total Weight                75% Total Weight           │
│   • Failure Mode            Rote memorization               Inability to execute       │
│   • Anti-Cheat Response     Time decay penalty ($M_t$)      Root padding penalty ($CS$)│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Breakdown of Differences:
1. **Source of Truth:**
   * *Knowledge:* Validated through educational transcripts (`degree`, `cgpa`, `institution`) and course completions (`certifications`).
   * *Skill:* Validated through demonstrable deliverables (`projects`), repository analytics (`github_metrics`), and verified supervisor reviews (`internships`).
2. **Cognitive Evaluation:**
   * *Knowledge Testing:* Evaluated via MCQs testing factual recall. Protected by a **linear time-decay multiplier ($M_t$)** that penalizes hesitation beyond 15 seconds.
   * *Skill Testing:* Evaluated via **dynamic AI viva scenarios** where candidates must troubleshoot edge cases, explain architectural trade-offs, and defend implementation choices.
3. **The Anti-Padding Penalty ($CS$):**
   * If a candidate boasts extensive theoretical knowledge on their resume ($R_s = 90$) but stumbles during the viva ($A_s = 35$), our non-linear algorithm identifies the inflation and slashes their verified confidence score ($CS$).

---

## 5. Alignment with Government of India (GoI) Frameworks

Skill Setu is built to be **100% compliant with national educational and skill mandates**:

### A. NSQF & NCVET (Ministry of Skill Development & Entrepreneurship)
The National Skills Qualifications Framework defines 5 outcome parameters for competency. Skill Setu maps to them directly:

| Official NSQF Dimension | Statutory Requirement | Skill Setu Implementation |
| :--- | :--- | :--- |
| **1. Professional Knowledge** | Factual & theoretical domain understanding | Evaluated via Time-Decayed MCQs and AI viva conceptual rubrics. |
| **2. Professional Skill** | Practical application and cognitive execution | Evaluated via **Project Evidence ($P_e$)** and active GitHub code analysis. |
| **3. Process Knowledge** | Understanding industry workflows & standards | Classified under the **`frameworks`** taxonomy tier (e.g., *GAAP, Agile, GST*). |
| **4. Core Skills** | Social, communication, and digital workplace literacy | Classified under the **`soft_skills`** and **`tools`** taxonomy tiers. |
| **5. Responsibility** | Autonomy, supervision, and execution quality | Tracked in the **Milestone Internship Tracker** via recruiter star ratings (1–5★). |

### B. NEP 2020 & NCrF (National Credit Framework)
* **One Nation, One Student ID (`apaar_id`):** Candidate profiles natively capture the 12-digit APAAR ID, ready for seamless synchronization with the national Academic Bank of Credits (`abc_id`).
* **NHEQF Qualification Levels:** Supports educational progression from **Level 4.5** (Undergraduate Certificate) through **Level 7.0/8.0** (Postgraduate/Doctoral).
* **Multidisciplinary Minors (`minor_specialization`):** Adheres to NEP 2020 guidelines by tracking cross-disciplinary studies (e.g., Computer Science majors minoring in FinTech or UI/UX).

### C. Industry Standards (NASSCOM FutureSkills Prime & WEF)
* **Skill Recency Factor ($E_r$):** Accounts for the rapid 2.5-year half-life of technical skills by weighting how recently a skill was utilized in production.
* **T-Shaped Professional Profiling:** Balances deep domain functional ability (`technical_skills`) with broad contextual awareness (`frameworks`, `soft_skills`).

---

## 6. Mathematical Formulas & Algorithmic Engine

### 1. Individual Skill Proficiency Weight ($W_s$)
Calculates the baseline competency score for any extracted skill:
$$W_s^{\text{base}} = (0.6 \times P_e) + (0.4 \times E_r)$$

* **$P_e$ (Project Evidence Score, 0–100):** Depth and complexity of the skill in projects/case studies. Boosted by **$+15$ points** if verified in active GitHub repositories.
* **$E_r$ (Experience Recency Score, 0–100):** Chronological recency and tenure of active application.

### 2. Additive Credential Multiplier
If the skill is validated by an active, recognized industry certification:
$$W_s = \min(100, \text{round}(W_s^{\text{base}} \times 1.15))$$

### 3. MCQ Linear Time-Decay Multiplier ($M_t$)
Penalizes hesitation and prevents external search engine lookups:

| Response Time ($t_s$) | Multiplier ($M_t$) | Interpretation |
| :--- | :--- | :--- |
| $\le 15\text{ seconds}$ | $1.0$ | Instant recall, no penalty |
| $15 - 60\text{ seconds}$ | $1.0 - 0.3 \times \left(\frac{t_s - 15}{45}\right)$ | Linear decay down to 70% |
| $> 60\text{ seconds}$ | $0.7$ | Capped at minimum baseline |

### 4. Progressive Cognitive Assessment Score ($A_s$)
Synthesizes syntax recall with deep architectural viva reasoning:
$$A_s = (0.3 \times \text{MCQ Average}) + (0.7 \times \text{Viva Rubric Average})$$

### 5. Capped-Root Plagiarism & Resume-Padding Penalty ($CS$)
Compares candidate resume claims ($R_s$) against tested cognitive capability ($A_s$). Excessive unverified claims trigger a non-linear penalty capped at a 40% reduction:
$$CS = A_s \times \left(1 - 0.4 \times \sqrt{\frac{\max(0, R_s - A_s)}{100}}\right)$$

### 6. Candidate Profile Strength Composite Score ($P_{\text{overall}}$)
Industry-standard composite score prioritizing applied skill (75%) over paper credentials (25%):
$$P_{\text{overall}} = (0.45 \times S_{\text{cognitive}}) + (0.30 \times S_{\text{projects\_exp}}) + (0.15 \times S_{\text{certifications}}) + (0.10 \times S_{\text{academics}})$$

* **$S_{\text{cognitive}}$ (45%):** Verified confidence score ($CS \in [0, 100]$).
* **$S_{\text{projects\_exp}}$ (30%):** Mean skill proficiency weight ($\overline{W_s}$), enriched with GitHub engineering production score.
* **$S_{\text{certifications}}$ (15%):** Credential volume ($1 \text{ cert} = 70, 2 \text{ certs} = 85, \ge 3 \text{ certs} = 100$).
* **$S_{\text{academics}}$ (10%):** Normalized academic performance ($(\text{CGPA} / 10.0) \times 100$).

### 7. Dynamic Role Fitment Score
Compares candidate skills matrix against database benchmarks:
$$\text{Role Fit Score} = (0.50 \times \text{Core Skills Score}) + (0.30 \times \text{Methodologies Score}) + (0.20 \times \text{Tooling Score})$$

---

## 7. SIH Presentation & Defense Highlights (Slide-Ready Bullets)

### Slide 1: The Core Innovation
* **Beyond Keyword ATS:** Skill Setu replaces unverified text matching with an autonomous cognitive evaluation engine.
* **The 75/25 Rule:** We allocate **75% of candidate ranking to demonstrated capability and problem solving**, and only 25% to passive academic credentials.

### Slide 2: Anti-Cheat & Integrity
* **Anti-Padding Penalty ($CS$):** A non-linear mathematical penalty that prevents candidates from gaming their profiles with buzzwords.
* **Zero-Unearned-Score Policy:** System faults or AI timeouts never grant unearned points. The platform schedules a secure retest to maintain verification integrity.
* **Anti-Vibe-Coding Radar:** Evaluates commits, CI/CD workflows, and test coverage to separate real engineers from prompt-only script copyists.

### Slide 3: Academic & Institutional Value (SIH Winning Factor)
* **Skill-Gap Radar for TPOs:** Real-time departmental analytics comparing employer demand with student competencies, pinpointing curriculum deficiencies.
* **Faculty Development (FDPs):** Dedicated discovery for professors to access corporate consultancies, faculty internships, and joint research.
* **Idempotent Placement Reporting:** Guaranteed database-level consistency for campus placement metrics.

### Slide 4: Social Impact & Inclusivity
* **Live Affirmative Action Radar:** Automated eligibility matching for national and corporate diversity initiatives (AICTE Pragati, TechSaksham, Adobe WIT, Tata AA).
* **Blind Screening (`blind=True`):** Redacts PII (Name, Gender, College) to eliminate cognitive bias while preserving verified capability scores.

### Slide 5: Robust Architecture
* **Hybrid 3-Signal NLP Search:** Deterministic skill overlap + 384d dense pgvector cosine similarity + PostgreSQL full-text SearchRank.
* **ACID Concurrency:** Row-level locks (`select_for_update`) ensure zero double-booking or application state deadlocks under high campus drive concurrency.
