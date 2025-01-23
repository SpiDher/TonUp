from aiogram.types import Message
from core.config import WELCOME_MESSAGE,Help_message
from aiogram.filters import CommandStart,Command
from core.loader import (
    bot,
    tc,
    router,
    logger
    )
from Data.schemas import UserCreate
from core.crud import create_user
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bot_handlers.windows import (connect_wallet_window,
                                  wallet_connected_window,
                                    send_transaction_window,
                                    timer,
                                    main_menu_windows,
                                    delete_last_message)
from core.config import recipient_address
from aiogram.fsm.context import FSMContext
from tonutils.tonconnect.models import Event
from tonutils.wallet.data import TransferData
from bot_handlers.utils import run_connection

 
@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Help handler for all messages"""
    current_message =await bot.send_message(chat_id=message.from_user.id,text=Help_message)
    #TODO - Check on the user_Id below and modify where neccesary
    await delete_last_message(message.from_user.id, current_message.message_id)
    

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    user= UserCreate(username=message.from_user.username,tg_id=message.from_user.id,fullname=message.from_user.full_name)
    await create_user(user=user)
    await main_menu_windows(user_id=message.from_user.id)

@router.callback_query()
async def call_back_handler(call_back_query:CallbackQuery,state: FSMContext):
    if call_back_query.data =='mint':
        await timer(call_back_query)
    elif call_back_query.data =='upgrade':
        connector = await tc.init_connector(call_back_query.from_user.id)
        rpc_request_id = (await state.get_data()).get("rpc_request_id")
        try:
            if connector.is_transaction_pending(rpc_request_id):
                connector.cancel_pending_transaction(rpc_request_id)
        except Exception as e:
            logger.error(f'Error: {e}')

        if not connector.connected:
            await connect_wallet_window(state, call_back_query.from_user.id)
        else:
            await wallet_connected_window(call_back_query.from_user.id)
    await call_back_query.answer()

@router.callback_query()
async def callback_query_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    connector = await tc.init_connector(callback_query.from_user.id)
    rpc_request_id = (await state.get_data()).get("rpc_request_id")

    if callback_query.data.startswith("app_wallet:"):
        selected_wallet = callback_query.data.split(":")[1]
        await state.update_data(selected_wallet=selected_wallet)
        await connect_wallet_window(state, callback_query.from_user.id)

    elif callback_query.data == "main_menu":
        await wallet_connected_window(callback_query.from_user.id)

    elif callback_query.data == "connect_wallet":
        await connect_wallet_window(state, callback_query.from_user.id)

    elif callback_query.data == "disconnect_wallet":
        connector.add_event_kwargs(Event.DISCONNECT, state=state)
        await connector.disconnect_wallet()

    elif callback_query.data == "cancel_transaction":
        if connector.is_transaction_pending(rpc_request_id):
            connector.cancel_pending_transaction(rpc_request_id)
        await wallet_connected_window(callback_query.from_user.id)

    elif callback_query.data == "send_transaction":
        rpc_request_id = await connector.send_transfer(
            destination=recipient_address,
            amount=0.000000001,
            body="Peniguin NFT Upgrade",
        )
        await send_transaction_window(callback_query.from_user.id)
        await state.update_data(rpc_request_id=rpc_request_id)

    elif callback_query.data == "send_batch_transaction":
        transfer_data = [
            TransferData(
                destination=recipient_address,
                amount=0.000000001,
                body="Peniguin NFT Upgrade",
            ) for _ in range(4)
        ]
        rpc_request_id = await connector.send_batch_transfer(transfer_data)
        await send_transaction_window(callback_query.from_user.id)
        await state.update_data(rpc_request_id=rpc_request_id)

    await callback_query.answer()
    



