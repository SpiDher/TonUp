from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    tg_id : int
    username : Optional[str]
    fullname: str
    admin_status: Optional[bool] = False

class UserShow(UserCreate):
    class Config:
        from_attributes = True
        



