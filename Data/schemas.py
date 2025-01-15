from pydantic import BaseModel

class UserData(BaseModel):
    id : int
    username : str
    fullname: str
    
class UserCreate(UserData):
    class Config:
        from_attributes = True
        


class Nelson():
    def __init__(self,stupid,dignity,thief):
        self.stupid= True
        self.dignity =False
        self.theif = True

