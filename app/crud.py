from . import models,schemas
from sqlalchemy.orm import session


def create_user(db:session, user:schemas.UserCreate):

    db_user = models.User(name  = user.name,
                          email = user.email
                         )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



def get_users(db:session):
    return db.query(models.User).all()