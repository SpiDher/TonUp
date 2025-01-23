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
import uvicorn
from fastapi import FastAPI
from core.loader import lifespan
from core.crud import create_user

app = FastAPI(lifespan=lifespan)

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


@app.post("/db")
async def root(request: UserCreate):
    """Health check endpoint"""
    # Query to check if the user already exists
    user = UserCreate(tg_id=request.tg_id,username=request.username,fullname=request.fullname)
    try:
        new_user = await create_user(user)
        print(new_user)
        return {'status':True}
    except Exception:
        return {'status':False}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)