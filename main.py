import os
import asyncio
from fastapi import FastAPI, HTTPException
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

# Initialize Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Create FastAPI app
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await client.start()
    print("Telegram Client Started")

@app.on_event("shutdown")
async def shutdown_event():
    await client.disconnect()
    print("Telegram Client Stopped")

@app.post("/add_members/")
async def add_members(group_username: str, user_ids: list):
    try:
        # Ensure client is connected
        if not client.is_connected():
            await client.connect()

        # Join the group
        await client(JoinChannelRequest(group_username))
        
        added_users = []
        for user_id in user_ids:
            try:
                await client(InviteToChannelRequest(group_username, [user_id]))
                added_users.append(user_id)
                await asyncio.sleep(5)  # Avoid Telegram rate limits
            except Exception as e:
                print(f"Error adding {user_id}: {e}")

        return {"status": "success", "added_users": added_users}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
