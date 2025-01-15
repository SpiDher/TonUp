from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey

class User(Base):
    __tablename__='User'
    id= Column(Integer,primary_key=True,index=True)
    username = Column(String)
    fullname = Column(String)
    
    

class Level(Base):
    __tablename__= 'Level'
    user = Column(String, ForeignKey('User.username'),primary_key=True)
    nft_level = Column(Integer)
    
    