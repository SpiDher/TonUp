from Data.models import User
from Data.schemas import UserCreate
from core.loader import logger
from sqlalchemy.future import select
from core.loader import get_db


async def create_user(user: UserCreate) -> bool:
    async for db in get_db():
        result = await db.execute(select(User).filter(User.Username == user.Username))
        existing_user = result.scalars().first()
        if not existing_user:
            new_user = User(Username=user.Username,Tg_id=user.Tg_id,Fullname=user.Fullname)
            logger.info(f"User {user.Fullname} created.")
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return True
    logger.info(f'User {user.Fullname} already exists')
    return False