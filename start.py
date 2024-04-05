from telethon import TelegramClient

api_id = 23563993
api_hash = "057691c0d92eca67cac9b395aaea25ac"
client = TelegramClient("anon", api_id, api_hash)


async def main():
    me = await client.get_me()
    print(me.stringify())

    async for dialog in client.iter_dialogs():
        print(dialog.name, "has ID", dialog.id)


with client:
    client.loop.run_until_complete(main())
