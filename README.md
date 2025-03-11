#TON Telegram Bot – Wallet Integration, Transactions & NFT Minting

Overview

This is a Telegram bot that integrates TON Wallet Connect, allowing users to manage their TON assets directly from Telegram. The bot enables users to send transactions, mint NFTs, and interact with the TON blockchain seamlessly.

Features

TON Wallet Connect Integration – Securely link and interact with a TON wallet.

Send TON Transactions – Transfer TON to other users directly via Telegram.

Mint NFTs – Mint and upgrade NFTs on the TON blockchain.

Real-time Notifications – Get updates on transaction status and NFT mints.

User-Friendly Interface – Simple commands for managing wallet activities.


Architecture

Telegram Bot (Aiogram + FastAPI) – Handles user interactions and commands.

TON Blockchain Integration – Communicates with the TON network for transactions and NFT minting.

Redis Storage – Caches user session data for faster processing.


Installation

Prerequisites

Python 3.10+

Redis

A TON Wallet API key


Steps

1. Clone the repository

git clone https://github.com/yourusername/ton-telegram-bot.git  
cd ton-telegram-bot


2. Install dependencies

pip install -r requirements.txt


3. Set environment variables

export BOT_TOKEN="your-telegram-bot-token"  
export TON_API_KEY="your-ton-api-key"  
export REDIS_URL="redis://localhost:6379"


4. Run the bot

python bot.py



Usage

1. Connect Wallet

Send /connect to link your TON wallet.



2. Check Balance

Use /balance to view your current TON balance.



3. Send TON

/send <amount> <recipient_address>



4. Mint NFT

/mint to create an NFT.

/upgrade to level up an existing NFT.



5. View Transactions

/history to check your latest transactions.




Future Enhancements

Support for multi-signature wallets.

Improved NFT marketplace integration.

Additional security features for transactions.
Bot is live at https://t.me/PenTonUp_bot
`Note:` It may take some time to respond 


Contributing

Feel free to open issues or submit pull requests.

License

MIT License.

