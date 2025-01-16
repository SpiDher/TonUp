from aiogram.types import Message
from core.config import WELCOME_MESSAGE,Help_message
from aiogram.filters import CommandStart,Command
from core.loader import logger,command_router
from Data.schemas import UserCreate
from core.crud import create_user
from sqlalchemy.ext.asyncio import AsyncSession


@command_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user= UserCreate(Username=message.from_user.username,Tg_id=message.from_user.id,Fullname=message.from_user.full_name)
    await create_user(user=user)
    await message.answer(f"Hello, {message.from_user.full_name}!\n{WELCOME_MESSAGE}")
    logger.info(f"User {message.from_user.full_name} started the bot.")
 
@command_router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Help handler for all messages"""
    await message.answer(Help_message)