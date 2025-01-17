from aiogram.types import Message
from core.config import WELCOME_MESSAGE,Help_message
from aiogram.filters import CommandStart,Command
from core.loader import logger,command_router
from Data.schemas import UserCreate
from core.crud import create_user
from core.loader import wallet_router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pytonconnect.exceptions import WalletNotConnectedError

from aiogram_tonconnect import ATCManager
from aiogram_tonconnect.tonconnect.models import ConnectWalletCallbacks

from bot_handlers.windows import UserState, select_language_window, main_menu_window


'''@command_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user= UserCreate(Username=message.from_user.username,Tg_id=message.from_user.id,Fullname=message.from_user.full_name)
    await create_user(user=user)
    await message.answer(f"Hello, {message.from_user.full_name}!\n{WELCOME_MESSAGE}")
    logger.info(f"User {message.from_user.full_name} started the bot.")'''
 
@command_router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Help handler for all messages"""
    await message.answer(Help_message)
    


@wallet_router.message(CommandStart())
async def start_command(message: Message, atc_manager: ATCManager) -> None:
    """
    Handler for the /start command.

    :param message: The Message object representing the incoming command.
    :param atc_manager: ATCManager instance for managing TON Connect integration.
    :return: None
    """
    user= UserCreate(Username=message.from_user.username,Tg_id=message.from_user.id,Fullname=message.from_user.full_name)
    await create_user(user=user)
    logger.info(f"User {message.from_user.full_name} started the bot.")
    # Calling up the language selection window
    await select_language_window(message.from_user, atc_manager)
    
@wallet_router.callback_query(UserState.select_language)
async def select_language_handler(call: CallbackQuery, atc_manager: ATCManager) -> None:
    """
    Handler for language selection callback.

    :param call: The CallbackQuery object representing the callback.
    :param atc_manager: ATCManager instance for managing TON Connect integration.
    :return: None
    """
    # Check if the call data is in supported languages:
    if call.data in ["ru", "en"]:
        # Updating the language in the aiogram-tonconnect interface
        await atc_manager.update_interfaces_language(call.data)

        # Create ConnectWalletCallbacks object 
        # with before_callback and after_callback functions
        callbacks = ConnectWalletCallbacks(
            before_callback=select_language_window,
            after_callback=main_menu_window,
        )
        # Open the connect wallet window using the ATCManager instance
        # and the specified callbacks
        await atc_manager.connect_wallet(callbacks)

    await call.answer()
    
@wallet_router.callback_query(UserState.main_menu)
async def main_menu_handler(call: CallbackQuery, atc_manager: ATCManager) -> None:
    """
    Handler for the main menu callback.

    :param call: The CallbackQuery object representing the callback.
    :param atc_manager: ATCManager instance for managing TON Connect integration.
    :return: None
    """
    # Check if the user clicked the "disconnect" button
    if call.data == "disconnect":
        # Check if wallet is connected before attempting to disconnect
        if atc_manager.tonconnect.connected:
            # Disconnect from the wallet
            await atc_manager.disconnect_wallet()

        # Create ConnectWalletCallbacks object with before_callback 
        # and after_callback functions
        callbacks = ConnectWalletCallbacks(
            before_callback=select_language_window,
            after_callback=main_menu_window,
        )

        # Open the connect wallet window using the ATCManager instance
        # and the specified callbacks
        await atc_manager.connect_wallet(callbacks)

    await call.answer()