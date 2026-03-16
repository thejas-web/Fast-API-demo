from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,HTTPException
from . import models,config
from .database import get_db

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES



# To read token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data:dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp":expire})

    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    
    except JWTError:
        return None
    


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)
                    ):
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")

    user_instance = db.query(models.User).filter(models.User.id==user_id).first()

    if not user_instance:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user_instance




    



