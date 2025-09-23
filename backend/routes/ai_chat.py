from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from middleware.isAuthenticated import get_current_user
from models.search_history import SearchHistory
from pydantic import BaseModel
from models.users import User
from models.competitors import Competitor
from langgraph_app.ai_chat_graph.nodes import web_Search
from langgraph_app.ai_chat_graph.state import ChatbotState
from langgraph_app.ai_chat_graph.graphs import build_chatbot_graph


router = APIRouter(prefix="/ai_chat", tags=["ai_chat"])

@router.get("/web_search")
def search_web():

    dummy_state = ChatbotState(
        query="",  # The query for your test
        user_id=26,
        competitor_ids=None,
        rag_results=None,  # No RAG results yet
        web_search_results=None, # No web search results yet
        top_k_rag=5,
        top_k_search=6,
        final_response="",  # Final response is empty initially
        should_end=False
    )

    res = web_Search(dummy_state)
    print(res)

    return None

class QueryRequest(BaseModel):
    query: str

@router.post("/")
async def call_chatbot_graph(request: QueryRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print("post endpoint for user query hit")

    competitor_ids_list = []
    for uc in user.user_competitors:
        competitor_ids_list.append(uc.competitor.competitor_id)
    
    init_state = ChatbotState(
        query= request.query,  
        user_id= user.user_id,
        competitor_ids= competitor_ids_list,
    )

    graph = build_chatbot_graph(ChatbotState)
    llm_ans = graph.invoke(init_state)
    
    return {"response": llm_ans['final_response']}

