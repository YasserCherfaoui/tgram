from telethon import TelegramClient

from app import api_hash, api_id

client = TelegramClient("anon", api_id=api_id, api_hash=api_hash)


async def main():
    async for dialog in client.iter_dialogs():
        print(type(dialog))


with client:
    client.loop.run_until_complete(main())
