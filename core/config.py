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
This is the official <b>Penguin NFT Bot</b>, Kindly connect your Ton wallet Below to get started.\n Choose any of the available options below to get started: \n run /start to see the options available to you \n run /help to see the options available to you \n run /connect to connect your wallet to the bot \n run /disconnect to disconnect your wallet from the bot \n run /balance to check your wallet balance \n run /mint to mint a new NFT \n run /transfer to transfer an NFT \n run /list to list all NFTs in your wallet \n run /details to get details of an NFT \n run /delete to delete an NFT \n run /update to update an NFT \n run /search to search for an NFT \n run /about to get information about the bot \n run /contact to get in touch with the developers \n run /exit to exit the bot'''
