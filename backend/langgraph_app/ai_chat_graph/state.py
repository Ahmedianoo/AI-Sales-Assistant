from typing import List, Dict, Optional
from pydantic import BaseModel
from services.schemas import SearchResult

class ChatbotState(BaseModel):
    query: str = ""
    user_id: int = None
    competitor_ids: Optional[List[int]] = None
    rag_results: Optional[List[SearchResult]] = None
    web_search_results: Optional[List[Dict]] =None
    top_k_rag: int = 3
    top_k_search: int = 1
    final_response: str = ""
    should_end: bool = False