from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import get_db
from models import RawDocument, UserCompetitor
from milvus.service import insert_embeddings, search
from milvus.schemas import SearchRequest
from services.ingest import process_and_ingest

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
def search_docs(req: SearchRequest, db: Session = Depends(get_db)):
    # Determine which competitor_ids are available for this user
    if not req.competitor_ids:
        competitor_ids = [
            uc.competitor_id
            for uc in db.query(UserCompetitor).filter(UserCompetitor.user_id == req.user_id).all()
        ]
    else:
        competitor_ids = req.competitor_ids

    # Search in Milvus
    hits = search(req.user_id, competitor_ids, req.query, req.top_k)

    # Map back to Postgres documents
    docs = db.query(RawDocument).filter(
        RawDocument.id.in_([h["doc_id"] for h in hits])
    ).all()

    results = [
        SearchResult(
            hit=h,
            text=next((d.text for d in docs if d.id == h["doc_id"]), None)
        )
        for h in hits
    ]

    return {"results": results}
