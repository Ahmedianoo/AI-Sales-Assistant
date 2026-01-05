from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.users import User
from models.battlecards import Battlecard  
from models.reports import Report         
from models.competitors import Competitor  
from models.user_competitor import UserCompetitor
from middleware.isAuthenticated import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)
@router.get("/")
def get_profile_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_id = current_user.user_id

        # Correct queries
        num_battlecards = (
            db.query(Battlecard)
            .join(UserCompetitor)
            .filter(UserCompetitor.user_id == user_id)
            .count()
        )

        num_reports = (
            db.query(Report)
            .join(UserCompetitor)
            .filter(UserCompetitor.user_id == user_id)
            .count()
        )

        num_competitors = (
            db.query(Competitor)
            .join(UserCompetitor)
            .filter(UserCompetitor.user_id == user_id)
            .count()
        )

        return {
            "user": {
                "id": current_user.user_id,
                "name": current_user.name,
                "email": current_user.email,
                "plan_type": current_user.plan_type
            },
            "stats": {
                "battlecards": num_battlecards,
                "reports": num_reports,
                "competitors": num_competitors
            }
        }

    except Exception as e:
        print("Profile fetch error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
