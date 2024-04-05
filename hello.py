from telethon import TelegramClient

api_id = 23563993
api_hash = "057691c0d92eca67cac9b395aaea25ac"

with TelegramClient("anon", api_id, api_hash) as client:
    client.loop.run_until_complete(
        client.send_message("YasserCherfaoui", "Hello, Myself!")
    )
