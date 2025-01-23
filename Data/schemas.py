from pydantic import BaseModel

class UserCreate(BaseModel):
    tg_id : int
    username : str
    fullname: str

class UserShow(UserCreate):
    class Config:
        from_attributes = True
        



