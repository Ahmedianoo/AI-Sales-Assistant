from pydantic import BaseModel
from typing import Dict, Any, Optional

class SearchResult(BaseModel):
    hit: Dict[str, Any]
    text: Optional[str]