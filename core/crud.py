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
            new_user = User(username=user.username,tg_id=user.tg_id,fullname=user.fullname)
            logger.info(f"User {user.fullname} created.")
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            logger.info(new_user)
            return True
    logger.info(f"User {user.fullname} already exists.")
    return False

async def get_user_by_id(tg_id:int) -> User:
    async for db in get_db():
        result = await db.execute(select(User).filter(User.tg_id == tg_id))
        user = result.scalar().first()
        return user
    
async def update_user_level(tg_id:int) -> bool:
    user = await get_user_by_id(tg_id)
    if user:
        user.level = int(user.level) + 1
        await user.commit()
        await user.refresh()
        return True

async def update_user_address(tg_id:int,address:str) -> bool:
    user = await get_user_by_id(tg_id)
    if user:
        user.address = address
        await user.commit()
        await user.refresh()
        return True
    return False