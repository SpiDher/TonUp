from dotenv import load_dotenv
import os
#Load environment variables
load_dotenv()
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
Token = os.getenv('Token')
WEBHOOK_PATH = "/webhook"
BASE_WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEB_HOOK =f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
WELCOME_MESSAGE='''
This is the official Penguin NFT Bot, Kidly connect your Ton wallet Below to get started'''

Help_message='''
This is the official <b>Penguin NFT Bot</b>, Kindly connect your Ton wallet Below to get started.\n Choose any of the available options below to get started: \n run /start to see the options available to you \n run /help to see the options available to you '''

REDIS_DSN = os.getenv('REDIS_DSN')
EXCLUDE_WALLETS = ["mytonwallet"]
MANIFEST_URL = os.getenv('MANIFEST_URL')
recipient_address= os.getenv('WALLET_ADDRESS')
