from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import get_db
from models import RawDocument, UserCompetitor
from milvus.service import insert_embeddings, search
from milvus.schemas import SearchRequest
from services.ingest import process_and_ingest
from services.search import search_documents

router = APIRouter(tags=["business"])

class IngestDocRequest(BaseModel):
    competitor_id: int
    text: str


class IngestDocResponse(BaseModel):
    doc_id: int
    chunks: int

class SearchResult(BaseModel):
    hit: Dict[str, Any]
    text: Optional[str]

class SearchResponse(BaseModel):
    results: List[SearchResult]


@router.post("/ingest_doc", response_model=IngestDocResponse)
def ingest_doc(req: IngestDocRequest):
    doc_id, num_chunks = process_and_ingest(req.competitor_id, req.text)
    return {"doc_id": doc_id, "chunks": len(num_chunks)}


@router.post("/search_docs", response_model=SearchResponse)
def search_docs(req: SearchRequest):
    results = search_documents(req.user_id, req.competitor_ids, req.query, req.top_k)
    return {"results": results}
