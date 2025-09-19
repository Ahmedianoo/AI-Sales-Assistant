from models import RawDocument, UserCompetitor
from milvus.service import search
from db import SessionLocal
from typing import List 

 



def search_documents(user_id: int, competitor_ids: List[int], query: str, top_k: int = 5):
    from routes.ingest_search import SearchResult
    db = SessionLocal()
    try:
        if not competitor_ids:
            competitor_ids = [
                uc.competitor_id
                for uc in db.query(UserCompetitor).filter(UserCompetitor.user_id == user_id).all()
            ]

        # Search in Milvus
        hits = search(user_id, competitor_ids, query, top_k)

        if not hits:
            return []

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

        return results    
    finally:
        db.close()    