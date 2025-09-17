from typing import List, Optional
from pydantic import BaseModel
from routes.ingest_search import SearchResult


class BattlecardState(BaseModel):
    query: Optional[str] = ""
    user_id: int
    search_results: Optional[List[SearchResult]] = None
    competitor_ids: List[int] = []
    content: Optional[dict] = None
    top_k: int = 5

