from sentence_transformers import SentenceTransformer
from rag.config import EMBED_MODEL

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)   # loaded once, reused
    return _model


def vector_size():
    return get_model().get_sentence_embedding_dimension()   # 384 for MiniLM


def embed_texts(texts):
    vectors = get_model().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()