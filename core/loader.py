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
bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Create a router for Aiogram commands
inline_router = Router()
command_router = Router()

dp.include_router(inline_router)
dp.include_router(command_router)

