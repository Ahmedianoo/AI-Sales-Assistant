
from fastapi import Depends, HTTPException, Request, APIRouter
from sqlalchemy.orm import Session
from jose import jwt
from db import get_db
from models import User
import os
from dotenv import load_dotenv


load_dotenv()
jwt_secret = os.getenv("SECRET_KEY")

def get_current_user(request: Request, db: Session = Depends(get_db)):


    print("=== Incoming Request ===")
    print("Cookies:", request.cookies)
    print("Headers:", request.headers)
    
    token = request.cookies.get("jwt")

    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        user = db.query(User).filter(User.user_id == payload["user_id"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")