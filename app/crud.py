from . import models,schemas
from sqlalchemy.orm import session
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto"
                          )
def create_user(db:session, user:schemas.UserCreate):

    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(name  = user.name,
                          email = user.email,
                          password = hashed_password
                         )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db:session):
    return db.query(models.User).all()


def get_user_by_email(db:session, email:str):
    return db.query(models.User).filter(models.User.email==email).first()