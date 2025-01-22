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
import aiofiles
import json,os
from types import SimpleNamespace
from core.storage import FileStorage
# Your bot token

# List of wallets to exclude
EXCLUDE_WALLETS = []

storage = FileStorage('connection.json')
bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot)

wallet_router = Router()
tc = TonConnect(storage=storage, manifest_url=MANIFEST_URL)
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




class AttributeDict(SimpleNamespace):
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, AttributeDict(value))
            elif isinstance(value, list):
                setattr(self, key, [AttributeDict(item) if isinstance(item, dict) else item for item in value])
            else:
                setattr(self, key, value)

    def get(self, item, default=None):
        return getattr(self, item, default)
    
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, AttributeDict):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, AttributeDict) else item for item in value
                ]
            else:
                result[key] = value
        return result


async def get_wallets():
    async with aiofiles.open(os.path.join(os.path.dirname(__file__), 'wallets-v2.json'), 'r') as file:
        data = json.loads(await file.read())
        
        wallets = []
        for wallet in data:
            if wallet.get("bridge") and len(wallet["bridge"]) > 0:
                wallet["bridge_url"] = wallet["bridge"][0].get("url")
            else:
                wallet["bridge_url"] = None
                
            # Append the wallet as an AttributeDict object
            wallets.append(AttributeDict(wallet))
        
        return wallets