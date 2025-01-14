from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv('Token')
WEBHOOK_PATH = "/webhook"
BASE_WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEB_HOOK =f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
WELCOME_MESSAGE='''
This is the official Penguin NFT Bot, Kidly connect your Ton wallet Below to get started'''
