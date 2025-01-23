from core.loader import tc
from core.loader import logger
from bot_handlers.windows import connect_wallet_window,wallet_connected_window
from aiogram.fsm.context import FSMContext
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