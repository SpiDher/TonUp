from Data.models import User
from Data.schemas import UserData
from Data.database import SessionLocal
from core.loader import logger




def create_user( user:UserData):
    with SessionLocal() as db:
        result = db.query(User).filter(User.username == user.username).first()
        if not result:
            new_user = User(username=user.username, id=user.id, fullname=user.fullname)
            logger.info(f"User {user.fullname} created.")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        else:
            logger.info(f'User {user.fullname} already exists')
    
