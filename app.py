import curses
from time import sleep
from telethon.client.updates import traceback
from config import api_id, api_hash
from telethon import TelegramClient
from shared_data import SharedData
from shared_data.data_types import DialogsLayoutChild
from ui import UI


class App:
    def __init__(self) -> None:
        self.shared_data = SharedData()
        self.running = True
        self.client = TelegramClient("anon", api_id=api_id, api_hash=api_hash)
        try:
            self.client.start()
        except Exception:
            e_msg = traceback.format_exc()
            with open("error.log", "w") as elog:
                elog.write(e_msg)
        self.ui = UI(self.shared_data, self.client.is_connected())
        from keyboard_shortcuts import KeyboardShortcut

        self.keyboard_shortcuts = KeyboardShortcut(self)

    async def load_dialogs(self):
        i = 0
        self.shared_data.dialogs_layout = []
        async for dialog in self.client.iter_dialogs():
            if i < self.ui.scr_h - 2:
                self.ui.write_chat(i + 1, 2, dialog)
                self.shared_data.dialogs_layout.append(
                    DialogsLayoutChild(dialog, (i + 1, 2))
                )
            i += 1
            self.ui.refresh()

    async def update_ui(self):
        await self.load_dialogs()

    async def main(self):
        me = await self.client.get_me()
        if me.username is not None:
            self.ui.write_line(
                0,
                1,
                f"{me.username} -- Chats",
                len(me.username) + 10,
                flag=curses.A_BOLD,
            )
        try:
            while self.running:
                await self.load_dialogs()
        except Exception:
            self.destroy()
            w = traceback.format_exc()
            with open("error.log", "w") as file:
                file.write(w)

    def destroy(self):
        self.running = False
        self.ui.cleanup()
        self.keyboard_shortcuts.stop()

    def run(self):
        try:
            with self.client:
                self.client.loop.run_until_complete(self.main())
        except Exception:
            error_msg = traceback.format_exc()
            with open("error1.log", "w") as efile:
                efile.write(error_msg)
