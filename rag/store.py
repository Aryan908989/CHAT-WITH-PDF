from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from rag.config import QDRANT_PATH, TOP_K, MIN_SCORE
from rag.embedder import embed_texts, vector_size

_client = None


def get_client():
    """Local Qdrant allows only one client, so we create it once."""
    global _client
    if _client is None:
        _client = QdrantClient(path=QDRANT_PATH)
    return _client


def collection_exists(name):
    return get_client().collection_exists(name)


def count_points(name):
    return get_client().count(collection_name=name).count


def index_chunks(name, chunks, filename):
    client = get_client()
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=vector_size(), distance=Distance.COSINE),
    )

    vectors = embed_texts([c["text"] for c in chunks])

    points = [
        PointStruct(
            id=c["chunk_id"],
            vector=vec,
            payload={"text": c["text"], "page": c["page"], "filename": filename},
        )
        for c, vec in zip(chunks, vectors)
    ]
    client.upsert(collection_name=name, points=points)


def search(name, question, top_k=TOP_K, min_score=MIN_SCORE):
    query_vector = embed_texts([question])[0]
    result = get_client().query_points(
        collection_name=name,
        query=query_vector,
        limit=top_k,
        score_threshold=min_score,
        with_payload=True,
    )
    return [
        {
            "text": p.payload["text"],
            "page": p.payload["page"],
            "score": round(p.score, 3),
        }
        for p in result.points
    ]