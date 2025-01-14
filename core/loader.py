from aiogram import Dispatcher,Bot,Router
from core.config import Token,WEB_HOOK
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager



#Initializing the bot and dispatcher
@asynccontextmanager
async def lifespan(app:FastAPI):
    await bot.set_webhook(WEB_HOOK)
    print("Webhook has been set.")
    yield
    
    await bot.session.close()
app = FastAPI(lifespan=lifespan)

# Create Aiogram bot and dispatcher
bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Create a router for Aiogram commands
router = Router()
