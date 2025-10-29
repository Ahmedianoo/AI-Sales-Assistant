from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from sqlalchemy.orm import Session

from db import get_db
from models.competitors import Competitor
from models.user_competitor import UserCompetitor
from models.users import User
from middleware.isAuthenticated import get_current_user  # ✅ import your auth dependency

router = APIRouter(prefix="/competitors", tags=["competitors"])


class CompetitorIn(BaseModel):
    name: str
    website_url: HttpUrl
    industry: Optional[str] = None
    report_frequency: Optional[str] = "monthly"
    battlecard_frequency: Optional[str] = "monthly"


class CompetitorOut(CompetitorIn):
    competitor_id: int

    class Config:
        orm_mode = True


@router.post("/", response_model=CompetitorOut)
def create_competitor(
    payload: CompetitorIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ✅ use the logged-in user
):
    exists = (
        db.query(Competitor)
        .filter(Competitor.website_url == str(payload.website_url))
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Website already exists")

    # create main competitor
    c = Competitor(
        name=payload.name,
        website_url=str(payload.website_url),
        industry=payload.industry,
    )
    db.add(c)
    db.commit()
    db.refresh(c)

    # link competitor to user
    uc = UserCompetitor(
        user_id=current_user.user_id,  # ✅ use real logged-in user ID
        competitor_id=c.competitor_id,
        report_frequency=payload.report_frequency,
        battlecard_frequency=payload.battlecard_frequency,
    )
    db.add(uc)
    db.commit()

    return c


@router.get("/", response_model=List[CompetitorOut])
def list_competitors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ✅ get user
):
    results = (
        db.query(Competitor, UserCompetitor)
        .join(UserCompetitor, Competitor.competitor_id == UserCompetitor.competitor_id)
        .filter(UserCompetitor.user_id == current_user.user_id)  # ✅ filter by user
        .all()
    )

    competitors = []
    for c, uc in results:
        competitors.append({
            "competitor_id": c.competitor_id,
            "name": c.name,
            "website_url": c.website_url,
            "industry": c.industry,
            "report_frequency": uc.report_frequency,
            "battlecard_frequency": uc.battlecard_frequency,
        })
    return competitors


@router.put("/{competitor_id}", response_model=CompetitorOut)
def update_competitor(
    competitor_id: int = Path(...),
    payload: CompetitorIn = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ✅ get user
):
    # ensure competitor belongs to this user
    uc = (
        db.query(UserCompetitor)
        .filter(
            UserCompetitor.competitor_id == competitor_id,
            UserCompetitor.user_id == current_user.user_id,
        )
        .first()
    )

    if not uc:
        raise HTTPException(status_code=404, detail="Competitor not found or not yours")

    # update competitor
    c = (
        db.query(Competitor)
        .filter(Competitor.competitor_id == competitor_id)
        .first()
    )
    if not c:
        raise HTTPException(status_code=404, detail="Competitor not found")

    c.name = payload.name
    c.website_url = str(payload.website_url)
    c.industry = payload.industry

    uc.report_frequency = payload.report_frequency
    uc.battlecard_frequency = payload.battlecard_frequency

    db.commit()
    db.refresh(c)
    return c


@router.delete("/{competitor_id}")
def delete_competitor(
    competitor_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ✅ get user
):
    uc = (
        db.query(UserCompetitor)
        .filter(
            UserCompetitor.competitor_id == competitor_id,
            UserCompetitor.user_id == current_user.user_id,
        )
        .first()
    )

    if not uc:
        raise HTTPException(status_code=404, detail="Competitor not found or not yours")

    # delete relation first
    db.delete(uc)
    db.commit()

    # optional: delete competitor itself if not linked to others
    linked_users = (
        db.query(UserCompetitor)
        .filter(UserCompetitor.competitor_id == competitor_id)
        .count()
    )
    if linked_users == 0:
        c = db.query(Competitor).filter(Competitor.competitor_id == competitor_id).first()
        if c:
            db.delete(c)
            db.commit()

    return {"message": "Competitor deleted successfully"}
