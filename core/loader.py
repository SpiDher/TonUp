from aiogram import Dispatcher,Bot,Router
from core.config import Token,WEB_HOOK
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import logger
from Data.database import engine,Base
from Data.database import AsyncSessionLocal
from aiogram import Router
from aiogram import Dispatcher
from core.config import MANIFEST_URL
from aiogram import Bot, Dispatcher
from tonutils.tonconnect import TonConnect
from core.storage import FileStorage
# Your bot token

# List of wallets to exclude
EXCLUDE_WALLETS = []

storage = FileStorage('connection.json')
bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot)
router2 = Router()
# Initializing the TonConnect instance
tc = TonConnect(storage=storage, manifest_url=MANIFEST_URL)
router = Router()
dp.include_router(router)
dp.include_router(router2)


@asynccontextmanager
async def get_db():
    db = AsyncSessionLocal()
    try: 
        yield db
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()

#Initializing the bot and dispatcher
@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info('Models Migrated')
    await bot.set_webhook(WEB_HOOK)
    logger.info("Webhook has been set.")
    yield
    await bot.session.close()




