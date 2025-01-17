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
from aiogram_tonconnect import ATCManager

def setup_middleware(dp: Dispatcher, atc_manager: ATCManager):
    dp.message.middleware(atc_manager.middleware())
    dp.callback_query.middleware(atc_manager.middleware())

"""
Asynchronously acquires a database session for use within an async context manager.

This function is designed to be used with the `async with` statement to ensure that the database session is properly
managed and committed or rolled back, even in the event of an exception.

Parameters:
None

Returns:
AsyncSessionLocal: An instance of the database session, which can be used within an async context manager.

Example usage:

```python
async def some_async_function():
    async with get_db() as db:
        # Perform database operations using `db`
        result = await db.query(SomeModel).first()
        return result

"""
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

wallet_router = Router()

wallet_router.message.filter(F.chat.type == ChatType.PRIVATE)
wallet_router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)
# Create a router for Aiogram commands

command_router = Router()

dp.include_router(wallet_router)
dp.include_router(command_router)

atc_manager = ATCManager()
setup_middleware(dp, atc_manager)

