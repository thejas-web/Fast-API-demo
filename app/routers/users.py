from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException
from ..database import SessionLocal
from .. import crud, schemas,security
from ..database import get_db
from ..schemas import Login
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto"
                          )

router = APIRouter()




@router.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)
               ):
    
    return crud.create_user(db,user)


@router.get("/users")
def get_users(db: Session = Depends(get_db),
              current_user = Depends(security.get_current_user)
             ):
    
    return crud.get_users(db)


@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):

    user = crud.get_user_by_email(db,data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    if not pwd_context.verify(data.password,user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")        

    token = security.create_access_token({"sub":str(user.id)})

    return {"access_token":token,
            "token_type":"bearer"
           }

