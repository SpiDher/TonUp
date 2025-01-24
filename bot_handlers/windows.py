import base64,time
from contextlib import suppress
from typing import List
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hide_link, hcode
from core.crud import update_user_address
from tonutils.tonconnect import TonConnect
from tonutils.tonconnect.models import WalletApp, Event, EventError, SendTransactionResponse
from tonutils.tonconnect.utils.exceptions import TonConnectError, UserRejectsError, RequestTimeoutError
from core.loader import dp,bot,tc,logger
from core.config import WELCOME_MESSAGE
from aiogram.types import CallbackQuery
import asyncio
from core.loader import logger

async def delete_last_message(user_id: int, message_id: int) -> None:
    state = dp.fsm.resolve_context(bot, user_id, user_id)
    last_message_id = (await state.get_data()).get("last_message_id")

    if last_message_id is not None:
        with suppress(Exception):
            await bot.delete_message(chat_id=user_id, message_id=last_message_id)

    await state.update_data(last_message_id=message_id)
    
def main_menu()->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Mint NFT',callback_data='mint'),
                InlineKeyboardButton(text='Upgrade NFT',callback_data='upgrade'))
    builder.row(InlineKeyboardButton(text='Connect Wallet',callback_data='connect_wallet'),
                InlineKeyboardButton(text='Disconnect Wallet',callback_data='disconnect_wallet'))
    return builder.as_markup()

async def main_menu_windows(user_id:int)->None:
    message = await bot.send_message(chat_id=user_id,text=WELCOME_MESSAGE,reply_markup=main_menu())
    await delete_last_message(user_id,message.message_id)

def _connect_wallet_markup(
        wallets: List[WalletApp],
        selected_wallet: WalletApp,
        connect_url: str,
) -> InlineKeyboardMarkup:
    wallets_button = [
        *[
            InlineKeyboardButton(
                text=f"• {wallet.name} •" if wallet.app_name == selected_wallet.app_name else wallet.name,
                callback_data=f"app_wallet:{wallet.app_name}",
            ) for wallet in wallets
        ]
    ]
    connect_wallet_button = InlineKeyboardButton(
        text=f"Connect {selected_wallet.name}",
        url=connect_url,
    )
    builder = InlineKeyboardBuilder()
    builder.row(connect_wallet_button)
    builder.row(*wallets_button, width=2)
    builder.row(InlineKeyboardButton(text="Back", callback_data="back"))

    return builder.as_markup()


def _confirm_transaction_markup(url: str, wallet_name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Open {wallet_name}", url=url)],
            [InlineKeyboardButton(text=f"Cancel", callback_data="cancel_transaction")],
        ]
    )


def _choose_action_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Back", callback_data="back"))
    builder.row(InlineKeyboardButton(text="Send transaction", callback_data="send_transaction"))
    return builder.as_markup()


def _go_to_main_menu_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Main menu", callback_data="main_menu"))

    return builder.as_markup()


async def connect_wallet_window(state: FSMContext, user_id: int) -> None:
    try:
        connector = await tc.init_connector(user_id)
        state_data = await state.get_data()
        wallets = await tc.get_wallets()

        selected_wallet = state_data.get("selected_wallet", wallets[0].app_name)
        selected_wallet = next(w for w in wallets if w.app_name == selected_wallet)
        connect_url = await connector.connect_wallet(wallet_app=selected_wallet)

        qrcode_url = (
            f"https://qrcode.ness.su/create?"
            f"box_size=20&border=7&image_padding=20"
            f"&data={base64.b64encode(connect_url.encode()).decode()}"
            f"&image_url={base64.b64encode(selected_wallet.image.encode()).decode()}"
        )

        text = f"{hide_link(qrcode_url)}Connect your wallet!"
        reply_markup = _connect_wallet_markup(wallets, selected_wallet, connect_url)

        message = await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
        await delete_last_message(user_id, message.message_id)
    except Exception as e:
        logger.info('Error\n',e)

async def wallet_connected_window(user_id: int) -> None:
    connector = await tc.init_connector(user_id)
    wallet_address = connector.wallet.account.address.to_str(is_bounceable=False)
    await update_user_address(user_id,wallet_address)
    reply_markup = _choose_action_markup()
    text = f"Connected wallet:\n{hcode(wallet_address)}\n\n Proceed to make the Transaction"

    message = await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    await delete_last_message(user_id, message.message_id)


async def send_transaction_window(user_id: int) -> None:
    connector = await tc.init_connector(user_id)
    reply_markup = _confirm_transaction_markup(
        url=connector.wallet_app.direct_url,
        wallet_name=connector.wallet_app.name,
    )

    text = "Please confirm the transaction in your wallet."

    message = await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    await delete_last_message(user_id, message.message_id)


async def transaction_sent_window(user_id: int, transaction: SendTransactionResponse) -> None:
    text = (
        "Transaction sent!\n\n"
        f"Transaction msg hash:\n{hcode(transaction.hash)}\n"
        f"Transaction BoC:\n{hcode(transaction.boc)}\n"
    )
    reply_markup = _go_to_main_menu_markup()

    message = await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    await delete_last_message(user_id, message.message_id)


async def error_window(user_id: int, message_text: str, button_text: str, callback_data: str) -> None:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    reply_markup = builder.as_markup()

    message = await bot.send_message(chat_id=user_id, text=message_text, reply_markup=reply_markup)
    await delete_last_message(user_id, message.message_id)


@tc.on_event(Event.CONNECT)
async def connect_event(user_id: int) -> None:
    await wallet_connected_window(user_id)


@tc.on_event(EventError.CONNECT)
async def connect_error_event(error: TonConnectError, user_id: int) -> None:
    button_text, callback_data = "Try again", "connect_wallet"
    if isinstance(error, UserRejectsError):
        message_text = f"You rejected the wallet connection."
    elif isinstance(error, RequestTimeoutError):
        message_text = f"Connection request timed out."
    else:
        message_text = f"Connection error. Error: {error.message}"
    await error_window(user_id, message_text, button_text, callback_data)


@tc.on_event(Event.DISCONNECT)
async def disconnect_event(user_id: int) -> None:
    state = dp.fsm.resolve_context(bot, user_id, user_id)
    await main_menu_windows(user_id)


@tc.on_event(EventError.DISCONNECT)
async def disconnect_error_event(error: TonConnectError, user_id: int) -> None:
    button_text, callback_data = "Try again", "connect_wallet"
    if isinstance(error, UserRejectsError):
        message_text = f"You rejected the wallet disconnection."
    elif isinstance(error, RequestTimeoutError):
        message_text = f"Disconnect request timed out."
    else:
        message_text = f"Disconnect error. Error: {error.message}"

    await error_window(user_id, message_text, button_text, callback_data)


@tc.on_event(Event.TRANSACTION)
async def transaction_event(user_id: int, transaction: SendTransactionResponse) -> None:
    await transaction_sent_window(user_id, transaction)


@tc.on_event(EventError.TRANSACTION)
async def transaction_error_event(error: TonConnectError, user_id: int) -> None:
    button_text, callback_data = "Try again", "main_menu"
    if isinstance(error, UserRejectsError):
        message_text = f"You rejected the transaction."
    elif isinstance(error, RequestTimeoutError):
        message_text = f"Transaction request timed out."
    else:
        message_text = f"Transaction error. Error: {error.message}"

    await error_window(user_id, message_text, button_text, callback_data)




active_timers = {}

async def timer(call_back_query: CallbackQuery):
    SAND_TIMER_FRAMES = ["⏳", "⌛"]

    # Check if a timer is already running for this user
    if call_back_query.message.chat.id in active_timers:
        await call_back_query.message.answer("Please wait while we mint your NFT")
        return

    # Send initial message
    sent_message = await call_back_query.message.answer("⏳ Minting....")
    active_timers[call_back_query.message.chat.id] = True
    logger.info(active_timers)# Mark timer as active
    start_time = time.time()
    try:
        i = 0
        while time.time() - start_time <= 5:
            # Cycle through the sand timer frames
            frame = SAND_TIMER_FRAMES[i % len(SAND_TIMER_FRAMES)]
            i += 1
            await asyncio.sleep(1)  # Delay for animation effect
            await bot.edit_message_text(
                chat_id=call_back_query.message.chat.id,
                message_id=sent_message.message_id,
                text=frame
            )
            
        success_msg = await bot.send_message(
            chat_id=call_back_query.message.chat.id,
            text="NFT mint <b>Succesful✅</b>, Confirm in you walet.\n\n You can now upgrade your NFT",
            )
        await delete_last_message(sent_message.message_id,success_msg.message_id)

    except Exception as e:
        print(f"Error in sand timer: {e}")
    finally:
        # Clean up active timer state
        await delete_last_message(call_back_query.message.chat.id, sent_message.message_id)
        active_timers.pop(call_back_query.message.chat.id, None)