from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from middleware.isAuthenticated import get_current_user
from models.conversations import Conversation
from pydantic import BaseModel
from models.users import User
from uuid import UUID

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

# @router.get("/messages/")
# def get_conversation_messages(thread_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
#     thread_history = global_checkpointer.list({"configurable": {"thread_id": thread_id}})

#     for checkpoint in thread_history:
#         messages = checkpoint.checkpoint.get("channel_values", {}).get("messages", [])
#         for msg in messages:
#             if msg.type == "human":  # User messages
#                 print(f"Content: {msg.content}, Time: {checkpoint.ts}")

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
