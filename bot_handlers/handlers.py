from aiogram.types import Message
from core.config import WELCOME_MESSAGE,Help_message
from aiogram.filters import CommandStart,Command
from core.loader import (
    bot,
    tc,
    router,
    logger,
    router2,
    bot
    )
from Data.schemas import UserCreate
from core.crud import create_user
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bot_handlers.windows import (main_menu_windows,
                                  main_menu,
                                  delete_last_message)
from core.config import recipient_address
from aiogram.fsm.context import FSMContext
from tonutils.tonconnect.models import Event
from tonutils.wallet.data import TransferData

from bot_handlers.utils import callback_checks
 
@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Help handler for all messages"""
    current_message =await bot.send_message(chat_id=message.from_user.id,
                                            text=Help_message,
                                            reply_markup=main_menu())
    '''NOTE - Delete last messsage based on the user's ID and the last message ID saved to the state, NOTE the new message ID is saved to the state and only deleted on the next function call '''
    await delete_last_message(message.from_user.id, current_message.message_id)



@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    #NOTE Create a new user or skip if the user already exist by intantiating the UserCreate object
    user= UserCreate(username=message.from_user.username,tg_id=message.from_user.id,fullname=message.from_user.full_name)
    #NOTE Run the asynchronous function to create the user
    await create_user(user=user)
    await main_menu_windows(message.from_user.id)

@router.callback_query()
async def callback_query_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_checks(callback_query,state)
    await callback_query.answer()
    



