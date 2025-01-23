from Data.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String(35), unique=True)
    fullname: Mapped[str] = mapped_column(String(30), nullable=False)
    wallet_address: Mapped[str]=mapped_column(String(60),nullable=True)
    level: Mapped["Level"] = relationship(
        "Level", back_populates="user", cascade="all, delete-orphan"
    )

class Level(Base):
    __tablename__ = 'Level'
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'), primary_key=True)
    nft_level: Mapped[int] = mapped_column(Integer, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="level")
