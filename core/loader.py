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
from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram import Dispatcher
from core.config import REDIS_DSN,MANIFEST_URL
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from tonutils.tonconnect import TonConnect
from redis.asyncio import Redis
from core.storage import TCRedisStorage


# Your bot token
redis = Redis.from_url(REDIS_DSN,)
# List of wallets to exclude
EXCLUDE_WALLETS = []
tc_storage = TCRedisStorage(redis)

bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher( bot=bot)

wallet_router = Router()
tc = TonConnect(storage=tc_storage, manifest_url=MANIFEST_URL)
command_router = Router()
dp.include_router(wallet_router)
dp.include_router(command_router)


async def get_db():
    db = AsyncSessionLocal()
    try: 
        yield db
    except Exception:
        await db.rollback()
    finally:
        await db.commit()
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
app = FastAPI(lifespan=lifespan)

# Create Aiogram bot and dispatcher





