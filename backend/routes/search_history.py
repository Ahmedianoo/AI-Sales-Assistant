from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from db import get_db, ASYNC_DATABASE_URL
from middleware.isAuthenticated import get_current_user
from models.conversations import Conversation
from pydantic import BaseModel
from models.users import User
from uuid import UUID
from datetime import datetime, timezone
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langGraph_app.ai_chat_graph.graphs import build_chatbot_graph
from langGraph_app.ai_chat_graph.state import ChatbotState
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
    
    #saver = getattr(request.app.state, "saver", None)
    async_pool = getattr(request.app.state, "async_pool", None)
    
    async with async_pool.connection() as conn:
        saver = AsyncPostgresSaver(conn)  # single connection per session   
        chatbot_graph = build_chatbot_graph(ChatbotState, saver)    

    #chatbot_graph = getattr(request.app.state, "chatbot_graph", None)
    if chatbot_graph is None:
        raise HTTPException(status_code=500, detail="Chatbot graph not initialized")

    # Retrieve the saved conversation state for this thread
    thread_state = await chatbot_graph.aget_state({"configurable": {"thread_id": thread_id}})
    if not thread_state:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Extract the list of messages (already ordered chronologically)
    messages = thread_state.values.get("messages", [])
    formatted_messages = []

    for i, msg in enumerate(messages):
        # Determine if message came from user or AI
        if isinstance(msg, HumanMessage):
            is_user = True
        elif isinstance(msg, AIMessage):
            is_user = False
        else:
            # In case of other message types (SystemMessage, ToolMessage, etc.)
            continue

        formatted_messages.append({
            "id": f"{thread_id}-{i}",  # unique per-thread message ID
            "text": msg.content,
            "isUser": is_user,
            "timestamp": msg.additional_kwargs.get("timestamp", datetime.now(timezone.utc).isoformat())
        })
    print("formatted messages as sent to frontend: ", formatted_messages)
    return {"messages": formatted_messages}