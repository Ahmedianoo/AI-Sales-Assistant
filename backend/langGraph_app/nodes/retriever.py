from langGraph_app.state.report_state import ReportState
from milvus.service import search
from db import SessionLocal
from models import RawDocument
from services.cleaning import clean_text
import re

def deduplicate_docs(docs: list[str]) -> list[str]:
    """Remove duplicates by normalizing whitespace, case, and punctuation."""
    seen = set()
    unique = []
    for d in docs:
        normalized = re.sub(r"\s+", " ", d.strip().lower())  # lowercase + collapse spaces
        if normalized not in seen:
            seen.add(normalized)
            unique.append(d)  # keep original version
    return unique


def retrieve_docs(state: ReportState) -> ReportState:
    user_id = state["user_id"]
    competitor_ids = state["competitor_ids"]
    query = state.get("query", "latest report")

    results = search(user_id, competitor_ids, query, top_k=5)

    if not results:
        state["retrieved_docs"] = []
        state["error"] = "Competitor not found"
        return state

    db = SessionLocal()
    try:
        docs = []
        for hit in results:
            doc = db.query(RawDocument).filter(RawDocument.id == hit["doc_id"]).first()
            if doc and doc.text:
                cleaned = clean_text(doc.text)  # 👈 clean before saving
                if cleaned:
                    docs.append(cleaned)

        # ✅ Deduplicate before saving into state
        docs = deduplicate_docs(docs)

        state["retrieved_docs"] = docs
    finally:
        db.close()

    return state
