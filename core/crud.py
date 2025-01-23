from Data.models import User
from Data.schemas import UserCreate
from core.loader import logger
from sqlalchemy.future import select
from core.loader import get_db


async def create_user(user: UserCreate) -> bool:
    async for db in get_db():
        result = await db.execute(select(User).filter(User.username == user.username))
        existing_user = result.scalars().first()
        if not existing_user:
            new_user = User(tg_id =user.tg_id,fullname=user.fullname,username=user.username)
            logger.info(f"User {user.fullname} created.")
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return True
    logger.info(f'User {user.fullname} already exists')
    return False