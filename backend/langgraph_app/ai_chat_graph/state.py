from typing import List, Dict, Optional, TypedDict, Annotated
from pydantic import BaseModel
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage # Import BaseMessage
from langgraph.graph.message import add_messages # Import the reducer
from services.schemas import SearchResult

class ChatbotState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    query: str = ""
    user_id: int = None
    competitor_ids: Optional[List[int]] = None
    competitors_names: Optional[List[str]] = None
    rag_results: Optional[List[SearchResult]] = None
    web_search_results: Optional[List[Dict]] =None
    top_k_rag: int = 3
    top_k_search: int = 1
    final_response: str = ""
    should_end: bool = False