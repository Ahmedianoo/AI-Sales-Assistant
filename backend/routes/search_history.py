from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from middleware.isAuthenticated import get_current_user
from models.search_history import SearchHistory
from pydantic import BaseModel
from models.users import User


router = APIRouter(prefix="/search_history", tags=["search_history"])

@router.get("/")
def get_user_search_history(current_user: User= Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        history = (
            db.query(SearchHistory)
            .filter(SearchHistory.user_id == current_user.user_id)
            .order_by(SearchHistory.searched_at.desc())
            .all()
        )

        #print("inside try of get search query")

        return [
            {
                "search_id": h.search_id,
                "query": h.query,
                "searched_at": h.searched_at,
            }
            for h in history
        ]
    except Exception as e:
        print("Error fetching history:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch search history")


# Pydantic model for incoming POST data
class SearchCreate(BaseModel):
    query: str

@router.post("/")
def save_search(search: SearchCreate, current_user: User =Depends(get_current_user), db: Session = Depends(get_db)):
    print("POST endpoint hit")
    try:
        new_search = SearchHistory(
            user_id=current_user.user_id,
            query=search.query
        )
        db.add(new_search)
        db.commit()
        db.refresh(new_search)
        return {
            "search_id": new_search.search_id,
            "query": new_search.query,
            "searched_at": new_search.searched_at,
        }
    except Exception as e:
        print("Error saving search:", str(e))
        raise HTTPException(status_code=500, detail="Failed to save search")
