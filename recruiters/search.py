import re
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from django.db.models import F
from students.search import (
    generate_embedding,
    build_canonical_skill_map,
    infer_query_domain,
    COMMON_SKILL_SYNONYMS
)

def index_job_listing(listing) -> None:
    """
    Constructs denormalized search_corpus and computes 384-dim BGE dense embedding
    for a JobListing model instance, saving them to PostgreSQL.
    """
    comp_name = listing.company.name if listing.company else ""
    skills_text = " ".join(listing.required_skills or [])
    eligibility_text = " ".join(f"{k} {v}" for k, v in (listing.eligibility_criteria or {}).items())
    
    remote_tag = "Remote Work Available" if getattr(listing, 'is_remote', False) else "On-site / In-person"
    corpus_parts = [
        f"Title: {listing.title}",
        f"Company: {comp_name}",
        f"Role Type: {listing.role_type}",
        f"Location: {listing.location} ({remote_tag})",
        f"Compensation: {listing.stipend_or_ctc}",
        f"Required Skills: {skills_text}",
        f"Eligibility: {eligibility_text}",
        f"Description: {listing.description}"
    ]
    corpus = "\n".join(corpus_parts)
    listing.search_corpus = corpus

    try:
        embedding_vec = generate_embedding(corpus, is_query=False)
        listing.embedding = embedding_vec
    except Exception as e:
        print(f"[Search Engine] Warning: Failed to generate embedding for listing {listing.id}: {e}")

    listing.save(update_fields=['search_corpus', 'embedding'])

def compute_job_skill_overlap(
    query_skills: List[str],
    listing_skills: List[str],
    canonical_map: Optional[Dict[str, Any]] = None
) -> Tuple[float, List[str]]:
    """
    Computes deterministic skill overlap between candidate's query skills
    and job listing's required skills.
    """
    if not query_skills or not listing_skills:
        return 0.0, []

    if canonical_map is None:
        try:
            canonical_map = build_canonical_skill_map()
        except Exception:
            canonical_map = {}

    q_set = {s.lower().strip() for s in query_skills}

    # Also resolve through canonical skill aliases
    resolved_q = set()
    for s in q_set:
        resolved_q.add(s)
        if s in canonical_map:
            resolved_q.add(canonical_map[s]["canonical"].lower())
        if s in COMMON_SKILL_SYNONYMS:
            resolved_q.add(COMMON_SKILL_SYNONYMS[s].lower())

    matched = []
    for ls in listing_skills:
        l_norm = ls.lower().strip()
        canonical_l = canonical_map.get(l_norm, {}).get("canonical", l_norm).lower()
        synonym_l = COMMON_SKILL_SYNONYMS.get(l_norm, l_norm).lower()
        if l_norm in resolved_q or canonical_l in resolved_q or synonym_l in resolved_q:
            matched.append(ls)

    if not matched:
        return 0.0, []

    # Overlap relative to listing requirements and query skills
    score = len(matched) / max(1, len(listing_skills))
    return round(min(1.0, score), 4), matched

def rank_job_listings(
    query: str,
    limit: int = 10,
    role_type: Optional[str] = None,
    location: Optional[str] = None,
    is_remote: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Candidate NLP Job Search Engine:
    Ranks published job listings against student's natural language requirements.
    Uses three-signal fusion:
      1. Deterministic skill overlap (40%)
      2. Dense BGE-small semantic cosine similarity via pgvector (40%)
      3. Full-text ts_rank or token match (20%)
    """
    from recruiters.models import JobListing
    from pgvector.django import CosineDistance

    if not query or not query.strip():
        return {
            "query": query,
            "total_results": 0,
            "results": []
        }

    # Extract query skills and domain
    canonical_map = build_canonical_skill_map()
    inferred_sector, query_skills = infer_query_domain(query, canonical_map)

    # Base queryset: only published listings with valid/open deadlines
    from django.utils import timezone
    from django.db.models import Q
    qs = JobListing.objects.filter(
        status=JobListing.ListingStatus.PUBLISHED
    ).filter(
        Q(application_deadline__gte=timezone.now()) | Q(application_deadline__isnull=True)
    ).select_related('company', 'recruiter__user')

    if role_type:
        qs = qs.filter(role_type=role_type)
    if location:
        qs = qs.filter(location__icontains=location)
    if is_remote is not None:
        qs = qs.filter(is_remote=is_remote)

    # Dense semantic query embedding
    query_embedding = generate_embedding(query, is_query=True)

    # Check pgvector support
    has_pgvector = False
    try:
        qs = qs.annotate(cosine_dist=CosineDistance('embedding', query_embedding))
        _ = qs.first()
        has_pgvector = True
    except Exception:
        has_pgvector = False
        qs = JobListing.objects.filter(
            status=JobListing.ListingStatus.PUBLISHED
        ).filter(
            Q(application_deadline__gte=timezone.now()) | Q(application_deadline__isnull=True)
        ).select_related('company', 'recruiter__user')
        if role_type:
            qs = qs.filter(role_type=role_type)
        if location:
            qs = qs.filter(location__icontains=location)
        if is_remote is not None:
            qs = qs.filter(is_remote=is_remote)

    # Full-text search annotation
    has_fulltext = False
    try:
        from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
        sq = SearchQuery(query, config='english')
        sv = SearchVector('search_corpus', config='english')
        qs = qs.annotate(ft_rank=SearchRank(sv, sq))
        _ = qs.first()
        has_fulltext = True
    except Exception:
        has_fulltext = False

    listings = list(qs)
    scored_results = []

    for listing in listings:
        # Signal 1: Skill overlap
        skill_score, matched_skills = compute_job_skill_overlap(query_skills, listing.required_skills or [], canonical_map=canonical_map)

        # Signal 2: Dense Semantic
        if has_pgvector and hasattr(listing, 'cosine_dist') and listing.cosine_dist is not None:
            semantic_score = max(0.0, min(1.0, 1.0 - float(listing.cosine_dist)))
        elif listing.embedding:
            emb = np.array(listing.embedding, dtype=np.float32)
            q_emb = np.array(query_embedding, dtype=np.float32)
            dot = np.dot(q_emb, emb)
            norm = (np.linalg.norm(q_emb) * np.linalg.norm(emb)) + 1e-9
            semantic_score = max(0.0, min(1.0, float(dot / norm)))
        else:
            semantic_score = 0.0
        semantic_score = round(semantic_score, 4)

        # Signal 3: Full-text
        if has_fulltext and hasattr(listing, 'ft_rank') and listing.ft_rank is not None:
            raw_ft = float(listing.ft_rank)
            fulltext_score = min(1.0, raw_ft * 3.0)
        else:
            corpus_lower = (listing.search_corpus or "").lower()
            q_words = [w for w in re.findall(r"\w+", query.lower()) if len(w) > 2]
            if q_words:
                hits = sum(1 for w in q_words if w in corpus_lower)
                fulltext_score = min(1.0, hits / len(q_words))
            else:
                fulltext_score = 0.0
        fulltext_score = round(fulltext_score, 4)

        # Three-signal fusion
        match_score = round((0.40 * skill_score) + (0.40 * semantic_score) + (0.20 * fulltext_score), 4)

        scored_results.append({
            "id": listing.id,
            "title": listing.title,
            "role_type": listing.role_type,
            "status": listing.status,
            "stipend_or_ctc": listing.stipend_or_ctc,
            "location": listing.location,
            "is_remote": getattr(listing, 'is_remote', False),
            "application_deadline": getattr(listing, 'application_deadline', None),
            "tenure": listing.tenure or "",
            "open_positions": listing.open_positions,
            "required_skills": listing.required_skills or [],
            "eligibility_criteria": listing.eligibility_criteria or {},
            "description": listing.description,
            "company_id": listing.company.id if listing.company else 0,
            "company_name": listing.company.name if listing.company else "Unknown Company",
            "company_logo": listing.company.branding_logo_url if listing.company else "",
            "company_website": listing.company.website if listing.company else "",
            "company_headquarters": listing.company.headquarters if listing.company else "",
            "recruiter_id": listing.recruiter.id if listing.recruiter else 0,
            "recruiter_name": listing.recruiter.user.username if listing.recruiter else "Hiring Team",
            "recruiter_designation": listing.recruiter.designation if listing.recruiter else "Recruiter",
            "match_score": match_score,
            "skill_overlap_score": skill_score,
            "semantic_score": semantic_score,
            "fulltext_score": fulltext_score,
            "matched_skills": matched_skills,
        })

    # Sort descending by match_score
    scored_results.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "query": query,
        "total_results": len(scored_results),
        "results": scored_results[:limit]
    }
