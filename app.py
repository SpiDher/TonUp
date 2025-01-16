from core.config import logger
from fastapi import Request, HTTPException,Depends
from aiogram.types import Update
from core.loader import dp,bot,app
from core.config import WEBHOOK_PATH
from bot_handlers import handlers
from core.loader import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from Data.schemas import UserShow,UserCreate
from Data.models import User
from sqlalchemy.future import select



@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request) -> dict:
    """Handle incoming updates from Telegram"""
    try:
        json_data = await request.json()
        update = Update(**json_data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid update payload")
    return {"ok": True}


@app.post("/db", response_model=UserShow)
async def root(request: UserCreate, db: AsyncSession = Depends(get_db)) -> UserShow:
    """Health check endpoint"""
    # Query to check if the user already exists
    result = await db.execute(select(User).filter(User.Username == request.Username))
    existing_user = result.scalars().first()

    if not existing_user:
        # Create a new user
        new_user = User(username=request.Username, id=request.Tg_id, fullname=request.Fullname)
        logger.info(f"User {request.Fullname} created.")
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    # result= await db.execute(select(User))
    # users= result.scalars().all()
    # return users
