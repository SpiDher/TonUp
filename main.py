from core.config import logger
from fastapi import Request, HTTPException,Depends
from aiogram.types import Update
from core.loader import dp,bot
from core.config import WEBHOOK_PATH
from bot_handlers import handlers
from core.loader import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from Data.schemas import UserShow,UserCreate
from Data.models import User
from sqlalchemy.future import select
import uvicorn
from fastapi import FastAPI
from core.loader import lifespan

app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request) -> dict:
    """NOTE Handle incoming updates from Telegram"""
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
    """NOTE Health check endpoint for production and database test"""
    # Query to check if the user already exists
    result = await db.execute(select(User).filter(User.username == request.username))
    existing_user = result.scalars().first()

    if not existing_user:
        # Create a new user
        new_user = User(username=request.username, id=request.tg_id, fullname=request.fullname)
        logger.info(f"User {request.fullname} created.")
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)