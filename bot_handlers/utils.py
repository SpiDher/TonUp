from core.loader import tc,logger
from core.config import recipient_address
from bot_handlers.windows import (connect_wallet_window,
                                  main_menu_windows,
                                  timer,
                                  wallet_connected_window,
                                  send_transaction_window,
                                  timer)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from tonutils.tonconnect.models import Event
from tonutils.wallet.data import TransferData
from core.crud import get_user_by_id,get_admin_status
from aiogram import Bot
from contextlib import suppress

async def delete_user_message(bot:Bot,chat_id:int,message_id:int):
  with suppress(Exception):
    await bot.delete_message(chat_id,message_id)


async def run_connection(state:FSMContext,user_id:int):
    connector = await tc.init_connector(user_id)
    rpc_request_id = (await state.get_data()).get("rpc_request_id")
    try:
        if connector.is_transaction_pending(rpc_request_id):
            connector.cancel_pending_transaction(rpc_request_id)
    except Exception as e:
        logger.error(f'Error: {e}')

    if not connector.connected:
        await connect_wallet_window(state, user_id)
    else:
        await wallet_connected_window(user_id)
        
async def callback_checks(callback_query:CallbackQuery,state:FSMContext):
    connector = await tc.init_connector(callback_query.from_user.id)
    rpc_request_id = (await state.get_data()).get("rpc_request_id")
    if callback_query.data =='mint':
        await timer(callback_query)
    elif callback_query.data =='upgrade':
        admin_status = await get_admin_status(callback_query.from_user.id)
        if admin_status:
            #NOTE - Just upgrade the NFT level of the Admin user
            await timer(callback_query)
        else:
            #NOTE - Ensure wallet is connected before and confrim txn before upgrade
            await run_connection(state,callback_query.from_user.id)
            
    elif callback_query.data == "back":
        await main_menu_windows(callback_query.from_user.id)
        
    elif callback_query.data.startswith("app_wallet:"):
        selected_wallet = callback_query.data.split(":")[1]
        await state.update_data(selected_wallet=selected_wallet)
        await connect_wallet_window(state, callback_query.from_user.id)

    elif callback_query.data == "main_menu":
        await wallet_connected_window(callback_query.from_user.id)

    elif callback_query.data == "connect_wallet":
        if not connector.connected:
            await connect_wallet_window(state, callback_query.from_user.id)
        else:
            await callback_query.answer(text="Wallet already connected", show_alert=True)

    elif callback_query.data == "disconnect_wallet":
        if connector.connected:
            connector.add_event_kwargs(Event.DISCONNECT, state=state)
            await connector.disconnect_wallet()
            await callback_query.answer(text="Wallet disconnected", show_alert=True)
        else:
            await callback_query.answer(text="Wallet already disconnected", show_alert=True)

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