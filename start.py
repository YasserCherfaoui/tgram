from telethon import TelegramClient
from config import api_id, api_hash
from telegram_cli import main

client = TelegramClient("anon", api_id=api_id, api_hash=api_hash)

with client:
    client.loop.run_until_complete(main(client))
