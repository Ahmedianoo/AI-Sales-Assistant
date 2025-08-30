from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional, Any
import datetime
from models.battlecards import Battlecard
from models.user_competitor import UserCompetitor
from db import get_db 



router = APIRouter(
    prefix="/battlecards",
    tags=["battlecards"]
)


#-----Base------
class BattlecardBase(BaseModel):
    user_comp_id: int
    title: str
    content: dict
    auto_release: Optional[bool] = False


#-----Create-----

class BattlecardCreate(BattlecardBase):
    pass



#-----Update-----
class BattlecardUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[dict] = None 
    auto_release: Optional[bool] = None

#-----Read/Response------
class BattlecardOut(BattlecardBase):
    battlecard_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


#----Base----
class UserCompetitorBase(BaseModel):
    report_frequency: str | None = None
    battlecard_frequency: str | None = None    



#----Read/Response----
class CompetitorOut(BaseModel):
    competitor_id: int
    name: str
    industry: str | None = None

    class Config:
        orm_mode = True

class UserCompetitorOut(UserCompetitorBase):
    user_comp_id: int
    user_id: int
    competitor: CompetitorOut   
    created_at: datetime.datetime

    class Config:
        orm_mode = True        



@router.get("/", response_model = List[BattlecardOut])
def get_battlecards(db: Session = Depends(get_db)):
    return db.query(Battlecard).all()  


@router.post("/", response_model = BattlecardOut)
def create_battlecard(battlecard: BattlecardCreate, db: Session = Depends(get_db)):
    new_battlecard = Battlecard(
        user_comp_id = battlecard.user_comp_id, 
        title = battlecard.title, 
        content = battlecard.content, 
        auto_release = battlecard.auto_release
    )
    db.add(new_battlecard)
    db.commit()
    db.refresh(new_battlecard)
    return new_battlecard


@router.get("/{id}", response_model = BattlecardOut)
def get_a_battlecard(id: int, db: Session = Depends(get_db)):
    battlecard = db.query(Battlecard).filter(Battlecard.battlecard_id == id).first()
    if not battlecard:
        raise HTTPException(status_code=404, detail="Battlecard not found")
    return battlecard


@router.put("/{id}", response_model = BattlecardOut)
def update_battlecard(id: int, battlecard_update: BattlecardUpdate, db: Session = Depends(get_db)):
    battlecard = db.query(Battlecard).filter(Battlecard.battlecard_id == id).first()
    if not battlecard:
        raise HTTPException(status_code=404, detail="Battlecard not found")
    
    updated_data = battlecard_update.dict(exclude_unset = True)

    for key ,value in updated_data.items():
        setattr(battlecard, key, value)

    db.commit()
    db.refresh(battlecard)
    return battlecard

@router.delete("/{id}", response_model=BattlecardOut)  
def delete_battlecard(id: int, db: Session = Depends(get_db)):
    battlecard = db.query(Battlecard).filter(Battlecard.battlecard_id == id).first()
    if not battlecard:
        raise HTTPException(status_code=404, detail="Battlecard not found")
    db.delete(battlecard)
    db.commit()

    return battlecard

    
    
    
@router.get("/user/{user_id}", response_model=List[UserCompetitorOut])
def get_user_competitors(user_id: int, db: Session = Depends(get_db)):
    competitors = db.query(UserCompetitor).filter(UserCompetitor.user_id == user_id).all()
    if not competitors:
        raise HTTPException(status_code=404, detail="No competitors found for this user")
    return competitors



@router.get("/competitor/{user_comp_id}", response_model=List[BattlecardOut])
def get_battlecards_for_competitor(user_comp_id: int, db: Session = Depends(get_db)):
    battlecards = db.query(Battlecard).filter(Battlecard.user_comp_id == user_comp_id).all()
    if not battlecards:
        raise HTTPException(status_code=404, detail="No battlecards found for this competitor")
    return battlecards














    