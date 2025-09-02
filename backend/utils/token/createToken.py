import datetime
from jose import jwt
import os
from dotenv import load_dotenv


load_dotenv()
jwt_secret = os.getenv("SECRET_KEY")

#create jwt token
def create_access_token(data: dict, expires_delta: int = 15):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, jwt_secret, algorithm="HS256")