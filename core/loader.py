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
from aiogram_tonconnect.handlers import AiogramTonConnectHandlers
from aiogram_tonconnect.middleware import AiogramTonConnectMiddleware

# Your bot token
storage = RedisStorage.from_url(REDIS_DSN)
# List of wallets to exclude
EXCLUDE_WALLETS = ["mytonwallet"]

bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

wallet_router = Router()

wallet_router.message.filter(F.chat.type == ChatType.PRIVATE)
wallet_router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)
# Create a router for Aiogram commands

command_router = Router()

dp.include_router(wallet_router)
dp.include_router(command_router)
async def main(): 

    # Creating a dispatcher object using the specified storage
    # Registering middleware for TON Connect processing
    dp.update.middleware.register(
        AiogramTonConnectMiddleware(
            redis=storage.redis,
            manifest_url=MANIFEST_URL,
            exclude_wallets=EXCLUDE_WALLETS,
            qrcode_type="url",  # or "bytes" if you prefer to generate QR codes locally.
        )
    )

    # Registering TON Connect handlers
    AiogramTonConnectHandlers().register(dp)


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
    await main()
    logger.info("Bot and dispatcher started.")
    logger.info("Webhook has been set.")
    yield
    await bot.session.close()
app = FastAPI(lifespan=lifespan)

# Create Aiogram bot and dispatcher





