from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from db import get_db
from middleware.isAuthenticated import get_current_user
from models.conversations import Conversation
from pydantic import BaseModel
from models.users import User
from models.competitors import Competitor
from langgraph_app.ai_chat_graph.nodes import web_Search
from langgraph_app.ai_chat_graph.state import ChatbotState
from uuid import UUID
from langgraph_app.ai_chat_graph.graphs import build_chatbot_graph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

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
    thread_id: UUID

@router.post("/")
async def call_chatbot_graph(
    request: QueryRequest,
    fastapi_request: Request, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)):

    print("post endpoint for user query hit")

    # Query to select the Conversation where the thread_id AND user_id match
    stmt = (
        select(Conversation)
        .where(
            and_(
                Conversation.thread_id == request.thread_id,
                Conversation.user_id == user.user_id 
            )
        )
    )
    conversation = db.execute(stmt).scalars().first()

    #if thread_id passed is not in conversations for the specific user 
    # --> add to db and invoke graph with init_sate        
    if not conversation:
        new_conversation = Conversation(
        thread_id=request.thread_id,
        user_id=user.user_id,
        title=request.query,
        # created_at is handled by the server_default in the model
        )

        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)

        competitor_ids_list = []
        for uc in user.user_competitors:
            competitor_ids_list.append(uc.competitor.competitor_id)
        
        init_state = ChatbotState(
            query= request.query,  
            user_id= user.user_id,
            competitor_ids= competitor_ids_list,
        )

        state_to_send = init_state
    #else if thread_id already found --> no db updates and invoke graph with message only
    else:
        state_to_send = {"query": request.query}

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    async_pool = getattr(fastapi_request.app.state, "async_pool", None)
    chatbot_graph = getattr(fastapi_request.app.state, "chatbot_graph", None)
    saver = getattr(fastapi_request.app.state, "saver", None)

    # async with async_pool.connection() as conn:
    #     saver = AsyncPostgresSaver(conn)  # single connection per session    
    llm_ans = await chatbot_graph.ainvoke(state_to_send, config, checkpointer=saver)
    
    return {"response": llm_ans['final_response']}

