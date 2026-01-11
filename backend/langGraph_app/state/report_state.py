from typing import List, Optional
from typing_extensions import TypedDict

class ReportState(TypedDict):
    user_id: int
    competitor_ids: List[int]
    query: Optional[str]
    retrieved_docs: Optional[List[str]]
    generated_report: Optional[str]
    error: Optional[str]
