"""Profile parsing and normalization."""
from pathlib import Path


def normalize_profile(text: str) -> str:
    lines = [" ".join(line.split()) for line in text.replace("\r", "").split("\n")]
    return "\n".join(line for line in lines if line)


def parse_pdf(file) -> str:
    from pypdf import PdfReader
    reader = PdfReader(file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return normalize_profile(text)


def parse_profile(text: str = "", uploaded_file=None) -> str:
    if uploaded_file is not None:
        name = uploaded_file.name.lower()
        if name.endswith(".pdf"):
            return parse_pdf(uploaded_file)
        return normalize_profile(uploaded_file.getvalue().decode("utf-8", errors="replace"))
    return normalize_profile(text)
