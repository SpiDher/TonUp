from Data.database import Base
from sqlalchemy import Integer, String,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from typing import Optional

class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[Optional[str]] = mapped_column(String(35), unique=True,nullable=True)
    fullname: Mapped[str] = mapped_column(String(30), nullable=False)
    nft_level:Mapped[Optional[int]] = mapped_column(Integer, default=0)
    address: Mapped[Optional[str]] = mapped_column(String(70), nullable=True)
    admin_status:Mapped[Optional[bool]] = mapped_column(Boolean)

    def __repr__(self):     
        return f"User {self.username} with id {self.tg_id} and address {self.address} created."
        