import os
from io import BytesIO
from pypdf import PdfReader
import docx

def parse_pdf(file_bytes: bytes) -> str:
    """Extracts raw text from a PDF binary stream."""
    reader = PdfReader(BytesIO(file_bytes))
    extracted_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text.append(text)
    return "\n".join(extracted_text)

def parse_docx(file_bytes: bytes) -> str:
    """Extracts raw text from a DOCX binary stream."""
    doc = docx.Document(BytesIO(file_bytes))
    extracted_text = []
    for paragraph in doc.paragraphs:
        if paragraph.text:
            extracted_text.append(paragraph.text)
    return "\n".join(extracted_text)

def parse_plain_text(file_bytes: bytes) -> str:
    """Decodes plain text (TXT, MD) binary stream into a UTF-8 string."""
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        # Fallback to latin-1 encoding if UTF-8 decoding fails
        return file_bytes.decode("latin-1")

def extract_text_from_file(file) -> str:
    """
    Polymorphic parser engine that inspects the file extension
    and extracts plain text in-memory. Supports PDF, DOCX, TXT, and MD.
    """
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
