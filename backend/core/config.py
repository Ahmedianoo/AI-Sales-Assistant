import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Local Milvus
    MILVUS_HOST: str = os.getenv("MILVUS_HOST", "milvus")
    MILVUS_PORT: str = os.getenv("MILVUS_PORT", "19530")

    # Cloud Milvus
    MILVUS_URI: str = os.getenv("MILVUS_URI")
    MILVUS_TOKEN: str = os.getenv("MILVUS_TOKEN")

    # Common
    MILVUS_COLLECTION: str = os.getenv("MILVUS_COLLECTION", "embeddings")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "384"))

    MILVUS_INDEX_TYPE: str = "HNSW"
    MILVUS_METRIC: str = "COSINE"
    MILVUS_HNSW_M: int = 16
    MILVUS_HNSW_EFCONSTRUCTION: int = 200

settings = Settings()
