from pydantic import BaseModel

class UserCreate(BaseModel):
    Tg_id : int
    Username : str
    Fullname: str

class UserShow(UserCreate):
    class Config:
        from_attributes = True
        



