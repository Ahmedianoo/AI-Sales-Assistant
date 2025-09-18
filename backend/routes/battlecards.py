from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from langgraph_app.battlecards_graph.graphs import battlecard_graph
from langgraph_app.battlecards_graph.state import BattlecardState
import datetime
from models.battlecards import Battlecard
from models.users import User
from models.user_competitor import UserCompetitor
from db import get_db 
from middleware.isAuthenticated import get_current_user



router = APIRouter(
    prefix="/battlecards",
    tags=["battlecards"]
)


#-----Base------
class BattlecardBase(BaseModel):
    user_comp_id: int
    title: str
    content: Optional[dict] = None
    auto_release: Optional[bool] = False


#-----Create-----

class BattlecardCreate(BaseModel):
    user_comp_id: int
    title: str
    query: Optional[str] = None
    auto_release: Optional[bool] = False



#-----Update-----
class BattlecardUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[dict] = None 
    auto_release: Optional[bool] = None

#-----Read/Response------
class BattlecardOut(BattlecardBase):
    battlecard_id: int
    created_at: Optional[datetime.datetime] = None
    competitor_name: Optional[str] = None

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
    created_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True        



@router.get("/", response_model=List[BattlecardOut])
def get_battlecards(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    battlecards = (
        db.query(Battlecard)
        .join(UserCompetitor, Battlecard.user_comp_id == UserCompetitor.user_comp_id)
        .filter(UserCompetitor.user_id == user.user_id)
        .order_by(Battlecard.created_at.desc())
        .all()
    )


    return [
        BattlecardOut(
            battlecard_id=bc.battlecard_id,
            user_comp_id=bc.user_comp_id,
            title=bc.title,
            content=bc.content,
            auto_release=bc.auto_release,
            created_at=bc.created_at,
            competitor_name=bc.user_competitor.competitor.name,  
        
        )
        for bc in battlecards
    ]




@router.post("/", response_model=BattlecardOut)
def create_battlecard(battlecard: BattlecardCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    user_competitor = db.query(UserCompetitor).filter(
        UserCompetitor.user_comp_id == battlecard.user_comp_id,
        UserCompetitor.user_id == user.user_id
    ).first()
    if not user_competitor:
        raise HTTPException(status_code=403, detail="Not authorized to use this competitor")
    

    initial_state = BattlecardState(
        query = battlecard.query or "",
        user_id = user.user_id,
        competitor_ids = [user_competitor.competitor_id],
        top_k = 5
    )


    final_state = battlecard_graph.invoke(initial_state)
    

    new_battlecard = Battlecard(
        user_comp_id=battlecard.user_comp_id, 
        title=battlecard.title, 
        content=final_state.content if final_state and final_state.content else {}, ##the content will be generated later based on the query 
        auto_release=battlecard.auto_release
    )
    db.add(new_battlecard)
    db.commit()
    db.refresh(new_battlecard)

    return BattlecardOut(
        battlecard_id=new_battlecard.battlecard_id,
        user_comp_id=new_battlecard.user_comp_id,
        title=new_battlecard.title,
        content=new_battlecard.content,
        auto_release=new_battlecard.auto_release,
        created_at=new_battlecard.created_at,
        competitor_name=new_battlecard.user_competitor.competitor.name
    )



@router.get("/{id}", response_model=BattlecardOut)
def get_a_battlecard(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    battlecard = db.query(Battlecard).filter(Battlecard.battlecard_id == id).first()
    if not battlecard:
        raise HTTPException(status_code=404, detail="Battlecard not found")

    if battlecard.user_competitor.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this battlecard")    
    
    return BattlecardOut(
        battlecard_id=battlecard.battlecard_id,
        user_comp_id=battlecard.user_comp_id,
        title=battlecard.title,
        content=battlecard.content,
        auto_release=battlecard.auto_release,
        created_at=battlecard.created_at,
        competitor_name=battlecard.user_competitor.competitor.name
    )



@router.put("/{id}", response_model=BattlecardOut)
def update_battlecard(id: int, battlecard_update: BattlecardUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    battlecard = db.query(Battlecard).filter(Battlecard.battlecard_id == id).first()
    if not battlecard:
        raise HTTPException(status_code=404, detail="Battlecard not found")

    if battlecard.user_competitor.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this battlecard")

    
    updated_data = battlecard_update.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(battlecard, key, value)

    db.commit()
    db.refresh(battlecard)

    # Explicitly construct BattlecardOut with competitor name
    return BattlecardOut(
        battlecard_id=battlecard.battlecard_id,
        user_comp_id=battlecard.user_comp_id,
        title=battlecard.title,
        content=battlecard.content,
        auto_release=battlecard.auto_release,
        created_at=battlecard.created_at,
        competitor_name=battlecard.user_competitor.competitor.name
    )


@router.delete("/{id}", response_model=BattlecardOut)  
def delete_battlecard(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    battlecard = db.query(Battlecard).filter(Battlecard.battlecard_id == id).first()
    if not battlecard:
        raise HTTPException(status_code=404, detail="Battlecard not found")
    
    if battlecard.user_competitor.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this battlecard")
    
    response = BattlecardOut(
        battlecard_id=battlecard.battlecard_id,
        user_comp_id=battlecard.user_comp_id,
        title=battlecard.title,
        content=battlecard.content,
        auto_release=battlecard.auto_release,
        created_at=battlecard.created_at,
        competitor_name=battlecard.user_competitor.competitor.name
    )

    db.delete(battlecard)
    db.commit()

    return response


    
    
    
@router.get("/user/", response_model=List[UserCompetitorOut])
def get_user_competitors(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    competitors = db.query(UserCompetitor).filter(UserCompetitor.user_id == user.user_id).all()
    return competitors



@router.get("/competitor/{user_comp_id}", response_model=List[BattlecardOut])
def get_battlecards_for_competitor(user_comp_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    user_competitor = db.query(UserCompetitor).filter(
        UserCompetitor.user_comp_id == user_comp_id,
        UserCompetitor.user_id == user.user_id
    ).first()

    if not user_competitor:
        raise HTTPException(status_code=403, detail="Not authorized to view battlecards for this competitor")


    battlecards = db.query(Battlecard).filter(Battlecard.user_comp_id == user_comp_id).order_by(Battlecard.created_at.desc()).all()

    return [
        BattlecardOut(
            battlecard_id=bc.battlecard_id,
            user_comp_id=bc.user_comp_id,
            title=bc.title,
            content=bc.content,
            auto_release=bc.auto_release,
            created_at=bc.created_at,
            competitor_name=bc.user_competitor.competitor.name,
        )
        for bc in battlecards
    ]















    