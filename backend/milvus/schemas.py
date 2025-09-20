from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    competitor_id: int
    doc_id: int
    chunks: List[str]

class SearchRequest(BaseModel):
    user_id: int
    competitor_ids: Optional[List[int]] = None
    query: str
    top_k: int = 5    
