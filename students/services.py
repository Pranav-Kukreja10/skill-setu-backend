import os
from io import BytesIO
from pypdf import PdfReader
import docx
from students.models import JobBenchmark

# --- IN-MEMORY MULTI-FILE PARSERS ---

def parse_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    extracted_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text.append(text)
    return "\n".join(extracted_text)

def parse_docx(file_bytes: bytes) -> str:
    doc = docx.Document(BytesIO(file_bytes))
    extracted_text = []
    for paragraph in doc.paragraphs:
        if paragraph.text:
            extracted_text.append(paragraph.text)
    return "\n".join(extracted_text)

def parse_plain_text(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1")

def extract_text_from_file(file) -> str:
    file_name = file.name.lower()
    file_bytes = file.read()
    
    if file_name.endswith('.pdf'):
        return parse_pdf(file_bytes).strip()
    elif file_name.endswith('.docx'):
        return parse_docx(file_bytes).strip()
    elif file_name.endswith(('.txt', '.md')):
        return parse_plain_text(file_bytes).strip()
    else:
        raise ValueError("Unsupported file format. Please upload a PDF, DOCX, TXT, or MD file.")

# --- DYNAMIC MULTI-DOMAIN BENCHMARKING MATCHING ENGINE ---

def calculate_role_score(extracted_skills: list, benchmark: JobBenchmark) -> int:
    """
    Calculates a normalized score (0-100) comparing extracted skills against 
    dynamic database job benchmarks.
    """
    extracted_lower = [s.lower() for s in extracted_skills]
    
    # Substring intersection matching to catch plural variations and edge cases
    matched_core = [s for s in benchmark.core_skills if any(s.lower() in ext for ext in extracted_lower)]
    matched_method = [s for s in benchmark.methodology_skills if any(s.lower() in ext for ext in extracted_lower)]
    matched_tooling = [s for s in benchmark.tooling_skills if any(s.lower() in ext for ext in extracted_lower)]
    
    core_score = (len(matched_core) / len(benchmark.core_skills)) * 100 if benchmark.core_skills else 0
    method_score = (len(matched_method) / len(benchmark.methodology_skills)) * 100 if benchmark.methodology_skills else 0
    tooling_score = (len(matched_tooling) / len(benchmark.tooling_skills)) * 100 if benchmark.tooling_skills else 0
    
    # Weighted Scoring Matrix: 50% Core Skills, 30% Methodologies, 20% Tooling & Software
    final_score = int((0.5 * core_score) + (0.3 * method_score) + (0.2 * tooling_score))
    return min(final_score, 100)

def generate_role_fit_matrix(extracted_skills: list) -> dict:
    """
    Generates the multi-role fitment scores dynamically using 
    active database benchmarks stored in PostgreSQL.
    """
    matrix = {}
    benchmarks = JobBenchmark.objects.select_related('sector').all()
    
    for benchmark in benchmarks:
        score = calculate_role_score(extracted_skills, benchmark)
        
        if score >= 75:
            fit_level = "High Match"
        elif score >= 40:
            fit_level = "Medium Match"
        else:
            fit_level = "Low Match"
            
        matrix[benchmark.role_title] = {
            "score": score,
            "fit_level": fit_level,
            "sector": benchmark.sector.name,
            "verified_confidence_score": None  # Will be populated when they pass the dynamic test
        }
    return matrix
