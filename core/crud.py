from Data.models import User
from Data.schemas import User
from sqlalchemy.orm import Session
from fastapi import Depends
from Data.database import SessionLocal
from Data.schemas import User

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
async def create_user(user_data:User,db:Session=Depends(get_db)):
    new_user = User(user_data)
    db.add(new_user)
    db.commit()
    db.refresh()
        
