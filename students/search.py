"""
Three-Signal Hybrid Search & Ranking System for Skill Setu

Architecture:
1. Skill-Tag Score (Deterministic, no ML):
   - Extract keywords from recruiter query.
   - Match to canonical skill tags via alias/synonym map built from StudentProfile.skills_matrix
     and JobBenchmark (core, methodology, tooling skills).
   - Sector/Domain context weighting: matched tags count higher when consistent with the query's
     inferred sector.
   - Score = sum(student skill weight x evidence) over matched tags, normalized.

2. Semantic Embedding Score:
   - Retrieval-tuned BAAI/bge-small-en-v1.5 (384 dimensions).
   - Singleton model loader in-process (never loaded per-request).
   - Denormalized search_corpus on StudentProfile weighted by skill confidence.
   - Generated at index time only. Never call embedding/LLM inside live query path.
   - pgvector brute-force cosine distance scan with index-ready structure.

3. Full-Text Score:
   - Postgres ts_rank against search_corpus for exact-match term recall.

Fusion:
   final_score = 0.4 * skill_tag_score + 0.4 * semantic_score + 0.2 * fulltext_score
"""

import os
import re
import math
import logging
from typing import List, Dict, Any, Optional, Tuple

from django.db.models import F
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

logger = logging.getLogger(__name__)

# Module-level singleton for BGE embedding model
_EMBEDDING_MODEL = None


def get_embedding_model():
    """
    Singleton loader for BAAI/bge-small-en-v1.5.
    Loaded once as a module-level object. Sub-15ms CPU/GPU inference.
    """
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Load BAAI/bge-small-en-v1.5 (384 dims, retrieval-tuned)
            _EMBEDDING_MODEL = SentenceTransformer("BAAI/bge-small-en-v1.5")
            logger.info("Successfully loaded BAAI/bge-small-en-v1.5 singleton model.")
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model: {e}")
            raise
    return _EMBEDDING_MODEL


def generate_embedding(text: str, is_query: bool = False) -> List[float]:
    """
    Generates a 384-dimensional unit-normalized embedding using BGE.
    For queries, prepends the standard BGE retrieval instruction.
    For document search_corpus, embeds clean raw text with no prefix.
    """
    model = get_embedding_model()
    if is_query:
        # Standard BGE instruction prefix for queries
        text = f"Represent this sentence for searching relevant passages: {text}"
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


# --- DOMAIN & ALIAS MAP BUILDER ---

COMMON_SKILL_SYNONYMS = {
    # IT & Software Engineering
    "py": "python",
    "python3": "python",
    "py3": "python",
    "postgres": "postgresql",
    "psql": "postgresql",
    "pg": "postgresql",
    "fast api": "fastapi",
    "rest": "rest api",
    "restful": "rest api",
    "rest apis": "rest api",
    "restful api": "rest api",
    "k8s": "kubernetes",
    "docker container": "docker",
    "containers": "docker",
    "qa": "quality assurance",
    "ci/cd": "cicd",
    "js": "javascript",
    "ts": "typescript",
    "reactjs": "react",
    "react.js": "react",
    "vuejs": "vue",
    "tailwind": "tailwind css",
    "html": "html5",
    "css": "css3",
    "dj": "django",
    
    # Mechanical Engineering
    "cad": "autocad",
    "solid works": "solidworks",
    "catia v5": "catia",
    "ansys workbench": "ansys",
    "finite element analysis": "fea",
    "gdt": "gd&t",
    "geometric dimensioning & tolerancing": "gd&t",
    "computational fluid dynamics": "cfd",
    "thermo": "thermodynamics",
    "fusion": "fusion 360",
    "autodesk fusion": "fusion 360",
    
    # Finance & Commerce
    "discounted cash flow": "dcf",
    "dcf analysis": "dcf",
    "financial models": "financial modeling",
    "ms excel": "excel",
    "spreadsheets": "excel",
    "sheets": "excel",
    "power bi": "powerbi",
    "tableau bi": "tableau",
    "bloomberg": "bloomberg terminal",
    "corp finance": "corporate finance",
    "valuation modeling": "valuation",

    # Accounting, Taxation & Auditing (B.Com / CA / CMA)
    "tally prime": "tally",
    "tally erp": "tally",
    "tally.erp 9": "tally",
    "quick books": "quickbooks",
    "gaap compliance": "gaap",
    "taxation": "tax",
    "tax filings": "tax",
    "gst filing": "gst",
    "gst portal": "gst",
    "tds filing": "tds",
    "financial audit": "auditing",
    "internal audit": "auditing",
    "book keeping": "bookkeeping",
    "ifrs standards": "ifrs",
    "costing": "cost accounting",
    "balance sheets": "financial reporting",
    
    # Business Administration, Management & Operations (BBA / MBA / HR)
    "biz dev": "business development",
    "operations": "operations management",
    "supply chain": "supply chain management",
    "scm": "supply chain management",
    "crm": "customer relationship management",
    "sales force": "salesforce",
    "swot": "swot analysis",
    "kpis": "kpi tracking",
    "kpi": "kpi tracking",
    "project mgmt": "project management",
    "pmp": "project management",
    "market research": "market analysis",
    "market study": "market analysis",
    "hr": "human resources",
    "hcm": "human resources",
    "talent": "talent acquisition",
    "recruitment": "talent acquisition",
    
    # Design & Creative Arts (UI/UX, Graphic Design)
    "ui design": "ui/ux",
    "ux design": "ui/ux",
    "user interface": "ui design",
    "user experience": "ux design",
    "wire framing": "wireframing",
    "proto typing": "prototyping",
    "adobe xd": "xd",
    "adobe ps": "photoshop",
    "adobe ai": "illustrator",
    "figma app": "figma",
    "design system": "design systems",
    "product design": "ui/ux",

    # Marketing & Growth
    "social media": "digital marketing",
    "smm": "digital marketing",
    "seo optimization": "seo",
    "search engine optimization": "seo",
    "sem": "search engine marketing",
    "google ads": "adwords",
    "content creation": "content marketing",
    "copy writing": "copywriting",
}

SECTOR_KEYWORDS = {
    "Information Technology": [
        "software", "developer", "backend", "frontend", "fullstack", "devops", "cloud",
        "api", "database", "web", "server", "python", "django", "react", "programming", "code",
        "tailwind", "javascript", "vite", "html", "css", "ui", "ux"
    ],
    "Mechanical Engineering": [
        "mechanical", "cad", "design", "solidworks", "autocad", "fea", "cfd", "stress",
        "aerospace", "fluid", "thermodynamics", "manufacturing", "automotive", "machining"
    ],
    "Finance & Commerce": [
        "finance", "analyst", "financial", "accounting", "valuation", "dcf", "banking",
        "equity", "investment", "portfolio", "excel", "balance sheet", "audit", "commerce",
        "tally", "gst", "tds", "tax", "ifrs", "gaap", "costing"
    ],
    "Business & Management": [
        "management", "bba", "mba", "operations", "supply chain", "strategy", "hr", "sales",
        "marketing", "business analyst", "project manager", "consultant", "recruitment"
    ],
    "Design & Creative Arts": [
        "designer", "design", "ui", "ux", "figma", "wireframe", "prototype", "illustrator",
        "photoshop", "creative", "branding", "product design", "visual"
    ]
}


def build_canonical_skill_map() -> Dict[str, Dict[str, Any]]:
    """
    Builds an alias/synonym map dynamically from all JobBenchmark skills
    and StudentProfile skills in the database, supplemented by COMMON_SKILL_SYNONYMS.
    Returns mapping:
        alias_or_skill_lower -> {
            "canonical": canonical_name,
            "sector": primary_sector_name,
            "category": "core" | "methodology" | "tooling" | "profile"
        }
    """
    from students.models import JobBenchmark, StudentProfile

    canonical_map = {}

    # 1. Gather all canonical skills from JobBenchmark
    try:
        benchmarks = JobBenchmark.objects.select_related("sector").all()
        for b in benchmarks:
            sector_name = b.sector.name
            for skill in b.core_skills:
                s_clean = skill.lower().strip()
                canonical_map[s_clean] = {"canonical": s_clean, "sector": sector_name, "category": "core"}
            for skill in b.methodology_skills:
                s_clean = skill.lower().strip()
                canonical_map[s_clean] = {"canonical": s_clean, "sector": sector_name, "category": "methodology"}
            for skill in b.tooling_skills:
                s_clean = skill.lower().strip()
                canonical_map[s_clean] = {"canonical": s_clean, "sector": sector_name, "category": "tooling"}
    except Exception as e:
        logger.warning(f"Could not load JobBenchmark for skill map: {e}")

    # 2. Gather additional skills from StudentProfiles
    try:
        profiles = StudentProfile.objects.only("skills_matrix", "role_fit_matrix").all()
        for p in profiles:
            p_sector = None
            if p.role_fit_matrix:
                for role_data in p.role_fit_matrix.values():
                    if isinstance(role_data, dict) and "sector" in role_data:
                        p_sector = role_data["sector"]
                        break
            if isinstance(p.skills_matrix, dict):
                for skill_key in p.skills_matrix.keys():
                    s_clean = skill_key.lower().strip()
                    if s_clean not in canonical_map:
                        canonical_map[s_clean] = {"canonical": s_clean, "sector": p_sector, "category": "profile"}
    except Exception as e:
        logger.warning(f"Could not load StudentProfiles for skill map: {e}")

    # 3. Add synonym mappings pointing to canonical names
    for alias, canonical in COMMON_SKILL_SYNONYMS.items():
        alias_clean = alias.lower().strip()
        canonical_clean = canonical.lower().strip()
        if canonical_clean in canonical_map:
            target_meta = canonical_map[canonical_clean]
            canonical_map[alias_clean] = {
                "canonical": canonical_clean,
                "sector": target_meta["sector"],
                "category": target_meta["category"]
            }
        else:
            canonical_map[alias_clean] = {
                "canonical": canonical_clean,
                "sector": None,
                "category": "synonym"
            }

    return canonical_map


def infer_query_domain(query: str, canonical_map: Dict[str, Dict[str, Any]]) -> Tuple[Optional[str], List[str]]:
    """
    Extracts keywords and canonical skill tags from the recruiter query.
    Infers the query's target domain/sector based on matched skills, sector names, and role keywords.
    Returns:
        (inferred_sector_name_or_none, list_of_matched_canonical_skills)
    """
    query_lower = query.lower()
    query_clean = re.sub(r"[^\w\s\+\#\-\.]", " ", query_lower)
    tokens = query_clean.split()

    matched_canonical = set()
    matched_sectors = []
    consumed_indices = set()

    # 1. Check n-grams (3, 2, 1) while tracking consumed token indices
    n = len(tokens)
    for length in (3, 2, 1):
        for i in range(n - length + 1):
            if any(idx in consumed_indices for idx in range(i, i + length)):
                continue
            phrase = " ".join(tokens[i : i + length]).strip()
            if phrase in canonical_map:
                item = canonical_map[phrase]
                canonical_name = item["canonical"]
                matched_canonical.add(canonical_name)
                if item.get("sector"):
                    matched_sectors.append(item["sector"])
                for idx in range(i, i + length):
                    consumed_indices.add(idx)

    # 2. Sector keyword counts (dynamically discover DB sectors)
    from students.models import IndustrySector
    try:
        db_sectors = list(IndustrySector.objects.values_list('name', flat=True))
    except Exception:
        db_sectors = []

    all_known_sectors = set(list(SECTOR_KEYWORDS.keys()) + db_sectors)
    sector_scores = {sector: 0 for sector in all_known_sectors}

    for sector, kw_list in SECTOR_KEYWORDS.items():
        for kw in kw_list:
            if re.search(r"\b" + re.escape(kw) + r"\b", query_lower):
                sector_scores[sector] += 2

    # Match tokens against sector name itself
    for sec in all_known_sectors:
        for word in re.split(r"[\s&/,]+", sec.lower()):
            if len(word) >= 3 and re.search(r"\b" + re.escape(word) + r"\b", query_lower):
                sector_scores[sec] += 3

    # Add votes from matched canonical skills
    for sec in matched_sectors:
        if sec in sector_scores:
            sector_scores[sec] += 3

    best_sector = None
    max_score = 0
    for sec, score in sector_scores.items():
        if score > max_score:
            max_score = score
            best_sector = sec

    return best_sector, list(matched_canonical)


# --- 1. SKILL-TAG SCORER (Deterministic, no ML) ---

def compute_skill_tag_score(
    student_skills_matrix: dict,
    query_skill_tags: List[str],
    inferred_sector: Optional[str],
    candidate_sectors: Optional[List[str]] = None
) -> Tuple[float, List[str]]:
    """
    Deterministic Skill-Tag Score (no ML):
    Score = sum(student skill weight x evidence x sector_factor) over matched tags, normalized.

    - Ws: individual skill proficiency weight (0-100)
    - Pe: active project evidence score (0-100)
    - Sector consistency:
      - If candidate belongs to the query's inferred domain: 1.25x boost.
      - If candidate has a cross-domain skill collision (different sector): 0.6x.
      - Default / unclassified: 1.0x baseline.

    Returns:
        (normalized_score in [0.0, 1.0], list_of_matched_student_skills)
    """
    if not query_skill_tags:
        return 0.0, []

    if not isinstance(student_skills_matrix, dict) or not student_skills_matrix:
        return 0.0, []

    candidate_skills_lower = {k.lower().strip(): v for k, v in student_skills_matrix.items()}
    matched_skills = []
    total_contribution = 0.0

    # Sector consistency factor
    sector_factor = 1.0
    if inferred_sector and candidate_sectors:
        if any(inferred_sector.lower() in cs.lower() for cs in candidate_sectors):
            sector_factor = 1.25  # Domain alignment boost
        else:
            sector_factor = 0.60  # Sector collision suppression

    for q_skill in query_skill_tags:
        q_clean = q_skill.lower().strip()
        matched_key = None

        # Direct match or exact substring match
        if q_clean in candidate_skills_lower:
            matched_key = q_clean
        else:
            for c_skill in candidate_skills_lower.keys():
                if q_clean == c_skill or q_clean in c_skill or c_skill in q_clean:
                    matched_key = c_skill
                    break

        if matched_key:
            matched_skills.append(matched_key)
            skill_info = candidate_skills_lower[matched_key]
            if isinstance(skill_info, dict):
                ws = float(skill_info.get("weight", 50))
                pe = float(skill_info.get("project_evidence", 50))
            else:
                ws = 50.0
                pe = 50.0

            # Weight x Evidence contribution: (Ws / 100) * (Pe / 100) in [0.0, 1.0]
            skill_val = (ws / 100.0) * (pe / 100.0) * sector_factor
            total_contribution += skill_val

    # Theoretical maximum: all query skills matched with 100 weight and 100 evidence with max boost (1.25)
    max_possible = len(query_skill_tags) * 1.25
    normalized_score = min(1.0, total_contribution / max_possible) if max_possible > 0 else 0.0

    return round(normalized_score, 4), matched_skills


# --- 2. DENORMALIZED SEARCH CORPUS BUILDER & INDEXER ---

def build_student_search_corpus(profile) -> str:
    """
    Builds the denormalized search_corpus text field on StudentProfile from
    skills_matrix, projects, bio, and role_fit_matrix.

    Weighted so higher-confidence skills have more influence:
    - High confidence skills (weight >= 70) are placed prominently and repeated
      to increase both transformer self-attention pooling weight and Postgres BM25/ts_rank.
    - Medium skills are placed in secondary sections.
    - Projects include title, technologies, and descriptions.
    """
    sections = []

    # 1. Skills Matrix with Confidence Weighting
    high_skills = []
    med_skills = []
    other_skills = []

    if isinstance(profile.skills_matrix, dict):
        for s_name, s_data in profile.skills_matrix.items():
            if isinstance(s_data, dict):
                weight = s_data.get("weight", 50)
                pe = s_data.get("project_evidence", 50)
                er = s_data.get("experience_recency", 50)
                if weight >= 70:
                    high_skills.append(f"{s_name} (Expert, Weight: {weight}, Evidence: {pe}%)")
                elif weight >= 40:
                    med_skills.append(f"{s_name} (Proficient, Weight: {weight})")
                else:
                    other_skills.append(f"{s_name} (Basic)")
            else:
                med_skills.append(str(s_name))

    if high_skills:
        # Repeating high-confidence skills boosts attention weighting and term frequency
        sections.append("Primary Core Skills: " + ", ".join(high_skills) + ". " + ", ".join(high_skills))
    if med_skills:
        sections.append("Secondary Skills: " + ", ".join(med_skills))
    if other_skills:
        sections.append("Additional Competencies: " + ", ".join(other_skills))

    # 2. Roles and Fitment Ratings
    if isinstance(profile.role_fit_matrix, dict):
        role_lines = []
        for role_name, r_info in profile.role_fit_matrix.items():
            if isinstance(r_info, dict):
                score = r_info.get("score", 0)
                fit_level = r_info.get("fit_level", "")
                sector = r_info.get("sector", "")
                role_lines.append(f"{role_name} in {sector} ({fit_level}, score: {score})")
        if role_lines:
            sections.append("Qualified Domain Roles: " + " | ".join(role_lines))

    # 3. Projects
    if isinstance(profile.projects, list):
        proj_lines = []
        for p in profile.projects:
            if isinstance(p, dict):
                title = p.get("title", "")
                tech = ", ".join(p.get("technologies", [])) if isinstance(p.get("technologies"), list) else p.get("technologies", "")
                desc = p.get("description", "")
                proj_lines.append(f"Project: {title}. Technologies: {tech}. Details: {desc}")
        if proj_lines:
            sections.append("Engineering Projects:\n" + "\n".join(proj_lines))

    # 4. Target Roles Candidate is Seeking
    if isinstance(profile.target_roles, list) and profile.target_roles:
        sections.append("Seeking Target Roles: " + ", ".join(profile.target_roles) + ". " + ", ".join(profile.target_roles))

    # 5. Academic Credentials
    acad = []
    if getattr(profile, 'institution', None):
        acad.append(f"Institution: {profile.institution}")
    if getattr(profile, 'department', None):
        acad.append(f"Department: {profile.department}")
    if getattr(profile, 'degree', None):
        acad.append(f"Degree: {profile.degree}")
    if getattr(profile, 'cgpa', None):
        acad.append(f"CGPA: {profile.cgpa}")
    if getattr(profile, 'graduation_year', None):
        acad.append(f"Graduation: {profile.graduation_year}")
    if acad:
        sections.append("Academic Credentials: " + " | ".join(acad))

    # 6. Categorized Competencies
    if isinstance(getattr(profile, 'skills_categorized', None), dict):
        cat_lines = []
        for cat_name, cat_list in profile.skills_categorized.items():
            if isinstance(cat_list, list) and cat_list:
                cat_lines.append(f"{cat_name.replace('_', ' ').title()}: {', '.join(cat_list)}")
        if cat_lines:
            sections.append("Categorized Competencies: " + " | ".join(cat_lines))

    # 7. Professional Experience & Title
    prof_details = []
    if getattr(profile, 'current_designation', None):
        prof_details.append(f"Current Role / Designation: {profile.current_designation}")
    if getattr(profile, 'experience_years', None) and profile.experience_years > 0:
        prof_details.append(f"Total Professional Experience: {profile.experience_years} years")
    if prof_details:
        sections.append("Professional Background: " + " | ".join(prof_details))

    # 8. Industry Certifications & Verified Credentials
    certs = getattr(profile, 'certifications', None)
    if isinstance(certs, list) and certs:
        cert_lines = []
        for c in certs:
            if isinstance(c, dict):
                c_name = c.get("name", "")
                c_issuer = c.get("issuer", "")
                c_skills = ", ".join(c.get("skills_covered", []))
                issuer_str = f" from {c_issuer}" if c_issuer else ""
                skills_str = f" (Skills: {c_skills})" if c_skills else ""
                cert_lines.append(f"Certified: {c_name}{issuer_str}{skills_str}")
            elif isinstance(c, str):
                cert_lines.append(f"Certified: {c}")
        if cert_lines:
            sections.append("Industry Certifications & Credentials: " + " | ".join(cert_lines) + ". " + " | ".join(cert_lines))

    # 9. Bio and Summary
    if profile.bio:
        sections.append(f"Professional Summary: {profile.bio}")

    return "\n\n".join(sections).strip()


def index_student_profile(profile) -> None:
    """
    INDEX-TIME TRIGGER:
    Builds the search_corpus, generates 384-dim BGE dense embedding,
    and saves to StudentProfile.
    Triggered only after grading / verification completes or during seeding.
    Never called in the live recruiter query path.
    """
    corpus = build_student_search_corpus(profile)
    embedding = generate_embedding(corpus, is_query=False)

    profile.search_corpus = corpus
    profile.embedding = embedding
    profile.save(update_fields=["search_corpus", "embedding"])
    logger.info(f"Successfully indexed profile for user '{profile.user.username}' ({len(embedding)} dims).")


# --- 3. SCORER IMPLEMENTATIONS (UNIT / PYTHON FALLBACKS) ---

def compute_semantic_score(query_embedding: List[float], student_embedding: List[float]) -> float:
    """
    Cosine similarity between normalized embeddings in [0.0, 1.0].
    Used when computing in Python memory or unit testing.
    """
    if not query_embedding or not student_embedding:
        return 0.0
    dot = sum(q * s for q, s in zip(query_embedding, student_embedding))
    # BGE embeddings are L2 normalized, so cosine sim = dot product
    # Map from [-1.0, 1.0] to [0.0, 1.0]
    return max(0.0, min(1.0, float(dot)))


def compute_fulltext_score(search_corpus: str, query_text: str) -> float:
    """
    Fallback term-frequency calculation in [0.0, 1.0] when Postgres full-text is simulated.
    """
    if not search_corpus or not query_text:
        return 0.0
    q_tokens = set(re.findall(r"\w+", query_text.lower()))
    c_tokens = re.findall(r"\w+", search_corpus.lower())
    if not q_tokens or not c_tokens:
        return 0.0
    matches = sum(1 for t in c_tokens if t in q_tokens)
    score = matches / (len(q_tokens) * 5.0)
    return min(1.0, round(score, 4))


# --- 4. THREE-SIGNAL FUSION ---

def fuse_scores(
    skill_tag_score: float,
    semantic_score: float,
    fulltext_score: float,
    weights: Tuple[float, float, float] = (0.4, 0.4, 0.2)
) -> float:
    """
    Computes final fused ranking score:
    final_score = 0.4 * skill_tag + 0.4 * semantic + 0.2 * fulltext
    """
    w_skill, w_semantic, w_fulltext = weights
    final = (w_skill * skill_tag_score) + (w_semantic * semantic_score) + (w_fulltext * fulltext_score)
    return round(final, 4)


def rank_student_profiles(
    query: str,
    limit: int = 10,
    w_skill: float = 0.4,
    w_semantic: float = 0.4,
    w_fulltext: float = 0.2,
    blind: bool = False
) -> Dict[str, Any]:
    """
    Executes the Three-Signal Fusion search pipeline:
    1. Deterministic skill keyword extraction & sector inference.
    2. Local query embedding via singleton BGE model (<15ms).
    3. Retrieval:
       - Uses pgvector CosineDistance brute-force scan if available.
       - Uses PostgreSQL SearchRank for full-text exact matches.
    4. Deterministic skill-tag scoring with sector context.
    5. Three-signal fusion and descending ranking.
    Supports blind: bool toggle to redact candidate PII for unbiased skill-first hiring.
    """
    from students.models import StudentProfile

    if not query or not query.strip():
        return {
            "query": query,
            "inferred_sector": None,
            "matched_query_skills": [],
            "weights_used": {"skill_tag": w_skill, "semantic": w_semantic, "fulltext": w_fulltext},
            "total_results": 0,
            "is_blind": blind,
            "results": []
        }

    # 1. Alias mapping & domain inference
    canonical_map = build_canonical_skill_map()
    inferred_sector, query_skills = infer_query_domain(query, canonical_map)

    # 2. Local Query Embedding (singleton in memory)
    query_embedding = generate_embedding(query, is_query=True)

    # 3. Query PostgreSQL Database
    has_pgvector = False
    try:
        from pgvector.django import CosineDistance
        # Test if pgvector extension is functioning on the queryset
        test_qs = StudentProfile.objects.exclude(embedding__isnull=True).annotate(
            dist=CosineDistance("embedding", query_embedding)
        )
        test_qs.first()
        has_pgvector = True
    except Exception as e:
        logger.warning(f"pgvector query annotation not available or failed: {e}. Falling back to in-memory cosine.")
        has_pgvector = False

    # Base queryset
    qs = StudentProfile.objects.select_related("user").all()

    # Full-text SearchVector & SearchRank
    has_fulltext = False
    try:
        search_vector = SearchVector("search_corpus", config="english")
        search_query = SearchQuery(query, config="english", search_type="websearch")
        qs = qs.annotate(ft_rank=SearchRank(search_vector, search_query, normalization=32))
        has_fulltext = True
    except Exception as e:
        logger.warning(f"Postgres SearchRank annotation failed: {e}. Falling back to corpus scanner.")
        has_fulltext = False

    if has_pgvector:
        from pgvector.django import CosineDistance
        qs = qs.annotate(cosine_dist=CosineDistance("embedding", query_embedding))

    profiles = list(qs)
    scored_results = []

    for profile in profiles:
        # Candidate sectors from role_fit_matrix
        cand_sectors = []
        if isinstance(profile.role_fit_matrix, dict):
            for r_data in profile.role_fit_matrix.values():
                if isinstance(r_data, dict) and "sector" in r_data:
                    cand_sectors.append(r_data["sector"])

        # Signal 1: Skill-tag score (deterministic, no ML)
        skill_score, matched_cand_skills = compute_skill_tag_score(
            student_skills_matrix=profile.skills_matrix,
            query_skill_tags=query_skills,
            inferred_sector=inferred_sector,
            candidate_sectors=cand_sectors
        )

        # Signal 2: Semantic score
        if has_pgvector and hasattr(profile, "cosine_dist") and profile.cosine_dist is not None:
            # CosineDistance = 1 - cosine_similarity
            semantic_score = max(0.0, min(1.0, 1.0 - float(profile.cosine_dist)))
        elif profile.embedding:
            semantic_score = compute_semantic_score(query_embedding, profile.embedding)
        else:
            semantic_score = 0.0
        semantic_score = round(semantic_score, 4)

        # Signal 3: Full-text score
        if has_fulltext and hasattr(profile, "ft_rank") and profile.ft_rank is not None:
            # SearchRank with normalization=32 yields score in [0.0, 1.0)
            raw_ft = float(profile.ft_rank)
            fulltext_score = min(1.0, raw_ft * 3.0)  # Scale modest rank up
        else:
            fulltext_score = compute_fulltext_score(profile.search_corpus, query)
        fulltext_score = round(fulltext_score, 4)

        # Base Three-Signal Relevance Fusion
        relevance_score = fuse_scores(
            skill_tag_score=skill_score,
            semantic_score=semantic_score,
            fulltext_score=fulltext_score,
            weights=(w_skill, w_semantic, w_fulltext)
        )

        # Verification & Cognitive Confidence Multiplier:
        # Up to +15% for 100% confidence score, +10% for passing verification test
        conf_ratio = max(0.0, min(1.0, (profile.overall_confidence_score or 0.0) / 100.0))
        verified_bonus = 0.10 if profile.is_verified else 0.00
        confidence_boost = 1.0 + (0.15 * conf_ratio) + verified_bonus

        # Target Role Intent Alignment Bonus:
        # +5% boost if recruiter query explicitly mentions one of candidate's target roles
        candidate_target_roles = profile.target_roles or []
        role_intent_bonus = 0.05 if any(tr.lower() in query.lower() for tr in candidate_target_roles) else 0.0

        total_multiplier = round(confidence_boost + role_intent_bonus, 4)
        final = round(relevance_score * total_multiplier, 4)

        username_display = f"Candidate #{profile.id}" if blind else profile.user.username
        email_display = "[REDACTED]" if blind else profile.user.email
        institution_display = "[REDACTED]" if (blind and profile.institution) else (profile.institution or None)
        bio_display = "[REDACTED]" if (blind and profile.bio) else profile.bio

        scored_results.append({
            "id": profile.id,
            "username": username_display,
            "email": email_display,
            "bio": bio_display,
            "skills_matrix": profile.skills_matrix,
            "raw_extracted_skills": getattr(profile, 'raw_extracted_skills', []) or [],
            "role_fit_matrix": profile.role_fit_matrix,
            "target_roles": candidate_target_roles,
            "institution": institution_display,
            "department": getattr(profile, 'department', '') or None,
            "overall_confidence_score": profile.overall_confidence_score,
            "is_verified": profile.is_verified,
            "is_blind": blind,
            "final_score": final,
            "skill_tag_score": skill_score,
            "semantic_score": semantic_score,
            "fulltext_score": fulltext_score,
            "verification_boost": total_multiplier,
            "matched_skills": matched_cand_skills,
            "inferred_sector": inferred_sector
        })

    # Sort descending by final fused score
    scored_results.sort(key=lambda x: x["final_score"], reverse=True)

    return {
        "query": query,
        "inferred_sector": inferred_sector,
        "matched_query_skills": query_skills,
        "weights_used": {"skill_tag": w_skill, "semantic": w_semantic, "fulltext": w_fulltext},
        "total_results": len(scored_results),
        "is_blind": blind,
        "results": scored_results[:limit]
    }

