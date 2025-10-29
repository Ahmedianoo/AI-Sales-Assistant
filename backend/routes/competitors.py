from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from sqlalchemy.orm import Session

from db import get_db
from models.competitors import Competitor
from models.user_competitor import UserCompetitor

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
):
    exists = db.query(Competitor).filter(Competitor.website_url == str(payload.website_url)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Website already exists")

    c = Competitor(
        name=payload.name,
        website_url=str(payload.website_url),
        industry=payload.industry,
    )
    db.add(c)
    db.commit()
    db.refresh(c)

    uc = UserCompetitor(
        user_id=1,  # مؤقتًا نخليها 1
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
):
    results = (
        db.query(Competitor, UserCompetitor)
        .join(UserCompetitor, Competitor.competitor_id == UserCompetitor.competitor_id)
        .filter(UserCompetitor.user_id == 1)  # مؤقتًا user_id = 1
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
):
    c = db.query(Competitor).filter(Competitor.competitor_id == competitor_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Competitor not found")

    # update main competitor fields
    c.name = payload.name
    c.website_url = str(payload.website_url)
    c.industry = payload.industry

    # update related frequencies
    uc = db.query(UserCompetitor).filter(
        UserCompetitor.competitor_id == competitor_id,
        UserCompetitor.user_id == 1
    ).first()

    if uc:
        uc.report_frequency = payload.report_frequency
        uc.battlecard_frequency = payload.battlecard_frequency

    db.commit()
    db.refresh(c)

    return c
