from Data.models import User
from Data.schemas import UserCreate
from core.loader import logger
from sqlalchemy.future import select
from core.loader import get_db

admins=['Jenny_yama','Penivera']
async def create_user(user: UserCreate) -> bool:
    admin_status = True if user.username in admins else False
    async with get_db() as db:
        result = await db.execute(select(User).filter(User.username == user.username))
        existing_user = result.scalars().first()
        if not existing_user:
            new_user = User(username=user.username,
                            tg_id=user.tg_id,
                            fullname=user.fullname,
                            admin=admin_status
                            )
            logger.info(f"User {user.fullname} created.")
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            logger.info(new_user)
            return True
    logger.info(f"User {user.fullname} already exists.")
    return False

async def get_user_by_id(tg_id:int) -> User:
    async with get_db() as db:
        result = await db.execute(select(User).filter(User.tg_id == tg_id))
        user = result.scalars().first()
        return user
    
async def update_user_level(tg_id:int) -> bool:
    async with get_db() as db:
        result = await db.execute(select(User).filter(User.tg_id == tg_id))
        target_user = result.scalars().first()

        if target_user:
            target_user.nft_level += 1  # Increment the user's level
            await db.commit()  # Commit the changes
            await db.refresh(target_user)  # Refresh the user instance
            return target_user

async def update_user_address(tg_id:int,address:str) -> bool:
    async with get_db() as db:
        result = await db.execute(select(User).filter(User.tg_id == tg_id))
        target_user = result.scalars().first()
        if target_user:
            target_user.address = address
            await db.commit()
            await db.refresh(target_user)
            return True
    return False

async def get_admin_status(tg_id:int) -> bool:
    async with get_db() as db:
        result = await db.execute(select(User).filter(User.tg_id == tg_id))
        target_user = result.scalars().first()
        return target_user.admin