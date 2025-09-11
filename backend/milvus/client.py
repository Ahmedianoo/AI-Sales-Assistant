from pymilvus import (
    connections, FieldSchema, CollectionSchema, DataType,
    Collection, utility
)
from core.config import settings


def connect():

    """Always connect to Zilliz Cloud."""
    connections.connect(
        alias="default",
        uri=settings.MILVUS_URI,
        token=settings.MILVUS_TOKEN
    )

    # """Connect to Milvus server (cloud first, fallback to local)."""
    # if settings.MILVUS_URI and settings.MILVUS_TOKEN:
    #     # Connect to Zilliz Cloud
    #     connections.connect(
    #         alias="default",
    #         uri=settings.MILVUS_URI,
    #         token=settings.MILVUS_TOKEN
    #     )
    # else:
    #     # Fallback to local Milvus
    #     connections.connect(
    #         alias="default",
    #         host=settings.MILVUS_HOST,
    #         port=settings.MILVUS_PORT
    #     )


def ensure_collection() -> Collection:
    """Ensure the collection exists, create if missing."""
    connect()
    name = settings.MILVUS_COLLECTION
    dim = settings.EMBEDDING_DIM

    if not utility.has_collection(name):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="competitor_id", dtype=DataType.INT64, is_primary=False),
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=False),   # reference to raw_documents
            FieldSchema(name="chunk_id", dtype=DataType.INT64, is_primary=False), # which chunk inside doc
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        ]
        schema = CollectionSchema(fields, description="Embeddings per competitor/chunk")
        coll = Collection(name=name, schema=schema)

        # build vector index (HNSW with cosine similarity)
        index_params = {
            "index_type": settings.MILVUS_INDEX_TYPE,
            "metric_type": settings.MILVUS_METRIC,
            "params": {
                "M": settings.MILVUS_HNSW_M,
                "efConstruction": settings.MILVUS_HNSW_EFCONSTRUCTION
            }
        }
        coll.create_index(field_name="embedding", index_params=index_params)
        coll.load()
        return coll

    # if already exists
    coll = Collection(name=name)
    if not coll.has_index():
        index_params = {
            "index_type": settings.MILVUS_INDEX_TYPE,
            "metric_type": settings.MILVUS_METRIC,
            "params": {
                "M": settings.MILVUS_HNSW_M,
                "efConstruction": settings.MILVUS_HNSW_EFCONSTRUCTION
            }
        }
        coll.create_index(field_name="embedding", index_params=index_params)
    coll.load()
    return coll


def create_partition_if_missing(competitor_id: int) -> str:
    """
    Create a partition per competitor.
    This way embeddings for the same competitor are grouped together,
    but not duplicated per user.
    """
    coll = ensure_collection()
    pname = f"competitor_{competitor_id}"
    if pname not in [p.name for p in coll.partitions]:
        coll.create_partition(pname)
    return pname
