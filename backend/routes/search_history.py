from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from db import get_db, ASYNC_DATABASE_URL
from middleware.isAuthenticated import get_current_user
from models.conversations import Conversation
from pydantic import BaseModel
from models.users import User
from uuid import UUID
import datetime
from langgraph_app.ai_chat_graph.graphs import build_chatbot_graph
from langgraph_app.ai_chat_graph.state import ChatbotState
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


router = APIRouter(prefix="/search_history", tags=["search_history"])

@router.get("/")
def get_user_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        conversations = (
            db.query(Conversation)
            .filter(Conversation.user_id == current_user.user_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )

        #print("inside try of get search query") 
        return [
            {
                "id": c.thread_id,
                "query": c.title,
                "created_at": c.created_at
            }
            for c in conversations
        ]
    except Exception as e:
        print("Error fetching history:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch search history")

@router.get("/messages")
async def get_conversation_messages(request: Request, thread_id: str = Query(...)):
    # Retrieve the compiled graph and saver from app.state
    chatbot_graph = getattr(request.app.state, "chatbot_graph", None)
    async_pool = getattr(request.app.state, "async_pool", None)
    saver = getattr(request.app.state, "saver", None) 

    # async with async_pool.connection() as conn:
    #     saver = AsyncPostgresSaver(conn)  # single connection per session
    
    if chatbot_graph is None or saver is None:
        raise HTTPException(status_code=500, detail="Chatbot graph or saver not initialized")

    saved_states = await saver.aget_tuple(
            {"configurable": {"thread_id": thread_id}}
        )
    
    messages = []

    for state in saved_states:
        # Only proceed if state has a checkpoint dict with channel_values
        checkpoint_dict = getattr(state, "checkpoint", None)
        print("checkpoint dict", checkpoint_dict, type(checkpoint_dict))
        
        # Some returned states are just dicts with 'channel_values' at top-level
        if checkpoint_dict is None and isinstance(state, dict):
            checkpoint_dict = state if "channel_values" in state else None
        
        if not checkpoint_dict:
            continue  # skip metadata-only states

        channel_values = checkpoint_dict.get("channel_values", {})
        print("channel_values", channel_values, type(checkpoint_dict))

        #channel_values = state.get("checkpoint", {}).get("channel_values", {})

        # Use a timestamp if available
        #timestamp_str = state.get("checkpoint", {}).get("ts")
        timestamp_str = checkpoint_dict.get("ts")  # or fallback
        if timestamp_str:
            timestamp = datetime.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        else:
            timestamp = datetime.datetime.utcnow()

        user_query = channel_values.get("query")
        print("user query", user_query)
        if user_query:
            messages.append({
                "id": f"{thread_id}-{timestamp}-user",
                "text": user_query,
                "isUser": True,
                "timestamp": timestamp.isoformat()
            })

        ai_response = channel_values.get("final_response")
        if ai_response:
            messages.append({
                "id": f"{thread_id}-{timestamp}-ai",
                "text": ai_response,
                "isUser": False,
                "timestamp": timestamp.isoformat()
            })

        # Sort by timestamp
        messages.sort(key=lambda x: x["timestamp"])
        print(messages)

    return {"messages": messages}

# # Pydantic model for incoming POST data
# class SearchCreate(BaseModel):
#     query: str

# @router.post("/")
# def save_search(search: SearchCreate, current_user: User =Depends(get_current_user), db: Session = Depends(get_db)):
#     #print("POST endpoint hit")
#     try:
#         new_search = SearchHistory(
#             user_id=current_user.user_id,
#             query=search.query
#         )
#         db.add(new_search)
#         db.commit()
#         db.refresh(new_search)
#         # thread_id, list of message objects {id, text, isUser, timestamp}
#         return {
#             "search_id": new_search.search_id,
#             "query": new_search.query,
#             "searched_at": new_search.searched_at,
#         }
#     except Exception as e:
#         print("Error saving search:", str(e))
#         raise HTTPException(status_code=500, detail="Failed to save search")
