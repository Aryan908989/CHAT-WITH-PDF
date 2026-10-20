from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
QDRANT_PATH = str(BASE_DIR / "qdrant_data")

EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "openai/gpt-oss-20b"

CHUNK_SIZE = 500       # characters
CHUNK_OVERLAP = 50     # characters
TOP_K = 4
MIN_SCORE = 0.25       # chunks scoring below this are dropped