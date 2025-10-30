from typing import List, Optional
from pymilvus import Collection
from sentence_transformers import SentenceTransformer
from core.config import settings
from milvus.client import ensure_collection, create_partition_if_missing

_model = SentenceTransformer(settings.EMBEDDING_MODEL)

def embed_texts(texts: List[str]) -> List[List[float]]:
    return _model.encode(texts, normalize_embeddings=(settings.MILVUS_METRIC=="IP")).tolist()

def insert_embeddings(
    competitor_id: int,
    doc_id: int,
    chunks: List[str]
) -> List[int]:
    coll: Collection = ensure_collection()
    partition_name = create_partition_if_missing(competitor_id)

    vectors = embed_texts(chunks)
    chunk_ids = list(range(len(chunks)))

    entities = [
        [competitor_id] * len(chunks),
        [doc_id] * len(chunks),
        chunk_ids,
        vectors
    ]

    mr = coll.insert(entities, partition_name=partition_name)
    coll.flush()
    return list(mr.primary_keys)

def search(
    user_id: int,
    competitor_ids: Optional[List[int]],
    query: str,
    top_k: int = 5
):
    coll = ensure_collection()
    qvec = embed_texts([query])

    expr = None
    if competitor_ids:
        expr = f"competitor_id in {competitor_ids}"

    print("SEARCH expr:", expr)
    print("Partition names:", [f"competitor_{cid}" for cid in competitor_ids] if competitor_ids else None)

    search_params = {"metric_type": settings.MILVUS_METRIC, "params": {"ef": 64}}
    results = coll.search(
        data=qvec,
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        expr=expr,
        partition_names=[f"competitor_{cid}" for cid in competitor_ids] if competitor_ids else None,
        output_fields=["competitor_id", "doc_id", "chunk_id"]
    )

    hits = []
    for hit in results[0]:
        hits.append({
            "pk": hit.id,
            "score": float(hit.distance),
            "competitor_id": hit.get("competitor_id"),
            "doc_id": hit.get("doc_id"),
            "chunk_id": hit.get("chunk_id")
        })
    return hits
