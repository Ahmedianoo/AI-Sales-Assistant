from fastapi import APIRouter, Response, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional, Any
import datetime
from models.users import User
from db import get_db 
import bcrypt
import datetime
from utils.token.createToken import create_access_token
from middleware.isAuthenticated import get_current_user



router = APIRouter(
    prefix="/users",
    tags=["users"]
)

import datetime
from typing import Optional
from pydantic import BaseModel


# ----- Base -----
class UserBase(BaseModel):
    name: Optional[str] = None
    email: str
    plan_type: Optional[str] = "free"


# ----- Create -----
class UserCreate(UserBase):
    password: str   

# ----- login -----
class LoginRequest(BaseModel):
    email: str
    password: str

# ----- Update -----
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    plan_type: Optional[str] = None


# ----- Read / Response -----
class UserOut(UserBase):
    user_id: int
    created_at: datetime.datetime

    # class Config:
    #     orm_mode = True
    
    model_config = { 
        "from_attributes": True
    }

class AuthResponse(BaseModel):
    token: str
    user: UserOut

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed.encode("utf-8"),
    )

#signup
@router.post("/signup", response_model=AuthResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    
    # ensure password <= 72 bytes (bcrypt limit)
    # hashed_password = pwd_context.hash(user.password[:72])
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=user.password,
        plan_type="free"
    )



    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token({"user_id": new_user.user_id})


    return {
        "token": token,
        "user": UserOut.model_validate(new_user) 
    }



# login
@router.post("/login", response_model=AuthResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not login_data.password == user.password_hash:
            raise HTTPException(status_code=400, detail="Invalid email or password")

        token = create_access_token({"user_id": user.user_id})
        # response.set_cookie(
        #     key="jwt",
        #     value=token,
        #     httponly=True,
        #     samesite="none",
        #     path = "/",
        #     secure=False,   # set True if HTTPS
        #     max_age=15 * 24 * 60 * 60  # 15 days
        # )

        return {
        "token": token,
        "user": UserOut.model_validate(user) 
    }

    except HTTPException:
        raise
    except Exception as e:
        print("Login error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")




# #logout
# @router.post("/logout")
# def logout_user(response: Response):
#     try:
#         response.delete_cookie(key="jwt")
#         return {"message": "Logged out successfully"}
#     except Exception as e:
#         # log the error if needed
#         print("Logout error:", str(e))
#         raise HTTPException(status_code=500, detail="Internal Server Error")
    


@router.get("/me")
def get_user_info(current_user: User = Depends(get_current_user)):
    return {
        "user": {
            "id": current_user.user_id,
            "name": current_user.name,
            "email": current_user.email,
        }
    }
