from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///./{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_async_engine(sqlite_url, connect_args=connect_args)

AsyncSessionLocal=async_sessionmaker(bind=engine)

Base = declarative_base()