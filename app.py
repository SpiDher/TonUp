from core.config import logger
from fastapi import Request, HTTPException
from aiogram.types import Update
from core.loader import dp,bot,app
from core.config import WEBHOOK_PATH
from Data.database import engine
from Data import models
from bot_handlers import handlers

models.Base.metadata.create_all(bind=engine)



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


@app.get("/")
async def root() -> dict:
    """Health check endpoint"""
    return {"message": "Bot is running"}
