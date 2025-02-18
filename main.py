import os
from telethon import TelegramClient

# Get API credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

# Initialize the Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    await client.start()
    print("Bot is running...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
