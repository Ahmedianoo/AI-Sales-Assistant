from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel
from milvus.client import ensure_collection
from milvus.schemas import IngestRequest, SearchRequest
from milvus.service import insert_embeddings, search

router = APIRouter(prefix="/milvus", tags=["milvus"])


class IngestResponse(BaseModel):
    inserted: int
    ids: List[int]

class SearchResponse(BaseModel):
    count: int
    results: List[Dict[str, Any]]


@router.get("/health")
def health() -> dict:
    ensure_collection()
    return {"status": "ok"}


@router.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest) -> IngestResponse:
    pks = insert_embeddings(req.competitor_id, req.doc_id, req.chunks)
    return {"inserted": len(pks), "ids": pks}


@router.post("/search", response_model=SearchResponse)
def search_api(req: SearchRequest) -> SearchResponse:
    hits = search(req.user_id, req.competitor_ids, req.query, req.top_k)
    return {"count": len(hits), "results": hits}
