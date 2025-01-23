from pydantic import BaseModel
from typing import Optional
class UserCreate(BaseModel):
    tg_id : int
    username : str
    fullname: str
    level:Optional[int] = 0
    wallet_address: Optional[str]=None

class UserShow(UserCreate):
    class Config:
        from_attributes = True
        



