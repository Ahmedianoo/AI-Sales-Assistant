from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.user_competitor import UserCompetitor
from models.users import User
from middleware.isAuthenticated import get_current_user

router = APIRouter(
    prefix="/competitors",
    tags=["competitors"]
)

@router.get("/")
def get_user_competitors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all competitors assigned to the logged-in user.
    Requires Authorization: Bearer <token>
    """
    user_competitors = (
        db.query(UserCompetitor)
        .filter(UserCompetitor.user_id == current_user.user_id)
        .all()
    )

    if not user_competitors:
        return []


    return [
        {
            "user_comp_id": uc.user_comp_id,
            "competitor_id": uc.competitor.competitor_id,
            "competitor_name": uc.competitor.name,
            "website_url": uc.competitor.website_url,
            "industry": uc.competitor.industry,
            "report_frequency": uc.report_frequency,
            "battlecard_frequency": uc.battlecard_frequency,
        }
        for uc in user_competitors
    ]
