from rag.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_pages(pages, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split each page into overlapping chunks, keeping the page number."""
    chunks = []
    chunk_id = 0
    step = chunk_size - overlap

    for p in pages:
        text = p["text"]
        for start in range(0, len(text), step):
            piece = text[start:start + chunk_size].strip()
            if len(piece) < 30:        # skip tiny leftovers
                continue
            chunks.append({"text": piece, "page": p["page"], "chunk_id": chunk_id})
            chunk_id += 1
    return chunks