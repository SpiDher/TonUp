from Data.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    Tg_id: Mapped[int] = mapped_column(Integer)
    Username: Mapped[str] = mapped_column(String(20), unique=True)
    Fullname: Mapped[str] = mapped_column(String(30), nullable=False)
    Level: Mapped["Level"] = relationship(
        "Level", back_populates="User", cascade="all, delete-orphan"
    )

class Level(Base):
    __tablename__ = 'Level'
    User_id: Mapped[int] = mapped_column(ForeignKey('User.id'), primary_key=True)
    NFT_level: Mapped[int] = mapped_column(Integer, nullable=False)
    User: Mapped["User"] = relationship("User", back_populates="Level")
