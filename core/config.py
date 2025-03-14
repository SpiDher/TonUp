from dotenv import load_dotenv
import os
#Load environment variables
load_dotenv()
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
Token = os.getenv('Token')
WEBHOOK_PATH = "/webhook"
BASE_WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEB_HOOK =f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
WELCOME_MESSAGE='''
This is the <b>Official Penguin NFT Bot</b>, Kindly click any button below,<b>Mint</> for the first time,\n <b>Upgrade</b> to increase NFT level'''

Help_message='''
This is the official <b>Penguin NFT Bot</b>, Kindly connect your Ton wallet Below to get started.\n Choose any of the available options below to get started: \n run /start to see the options available to you  '''

recipient_address= os.getenv('WALLET_ADDRESS')
REDIS_DSN = os.getenv('REDIS_DSN')
EXCLUDE_WALLETS = ["mytonwallet"]
MANIFEST_URL = os.getenv('MANIFEST_URL')

upgrade_costs ={
    
}