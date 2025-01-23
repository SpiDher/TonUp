from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    tg_id : int
    username : str
    fullname: str
    admin: bool

class UserShow(UserCreate):
    class Config:
        from_attributes = True
        



