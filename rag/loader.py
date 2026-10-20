from pypdf import PdfReader


def load_pdf(path):
    """Return a list of {"page": int, "text": str}. Empty pages are skipped."""
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": i, "text": text})
    return pages