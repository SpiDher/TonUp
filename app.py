import logging
from fastapi import Request, HTTPException
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
from core.loader import dp,router,bot,app
from core.config import WEBHOOK_PATH,WELCOME_MESSAGE
from Data.database import engine
from Data import models



models.Base.metadata.create_all(bind=engine)


dp.include_router(router)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handler for /start command"""
    '''user=User(
        id= message.from_user.id,
        username=  message.from_user.username
               )
    await create_user(user)'''
    
    await message.answer(f"Hello, {message.from_user.full_name}!\n{WELCOME_MESSAGE}")


@router.message()
async def echo_handler(message: Message) -> None:
    """Echo handler for all messages"""
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Unable to copy your message!")




@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request) -> dict:
    """Handle incoming updates from Telegram"""
    print(await request.json())
    try:
        json_data = await request.json()
        update = Update(**json_data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid update payload")
    return {"ok": True}


@app.get("/")
async def root() -> dict:
    """Health check endpoint"""
    return {"message": "Bot is running"}
