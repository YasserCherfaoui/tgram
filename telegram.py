import curses
from time import sleep
from telethon.client.updates import traceback
from config import api_id, api_hash
from telethon import TelegramClient
from shared_data import SharedData


class App:
    def __init__(s) -> None:
        s.client = TelegramClient("anon", api_id=api_id, api_hash=api_hash)
        s.shared_data = SharedData()

    def init_ui(s) -> None:
        s.stdscr = curses.initscr()
        s.scr_h, s.scr_w = s.stdscr.getmaxyx()
        s.chat_max_w = s.scr_w // 4
        s.messages_max_w = s.scr_w - s.chat_max_w - 1

    def draw_ui(s):
        s.init_ui()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        s.stdscr.keypad(True)
        s.stdscr.vline(0, s.chat_max_w, curses.ACS_VLINE, s.scr_h)

    def write_line(s, y: int, x: int, buffer: str, max: int, flag=curses.A_NORMAL):
        s.stdscr.addstr(y, x, " " * max)
        s.stdscr.addstr(y, x, buffer, flag)

    def write_chat(s, y: int, x: int, chat: str):
        s.write_line(y, x, chat, s.chat_max_w - 4)

    def write_message(s, y: int, x: int, message: str):
        s.write_line(y, x, message, s.messages_max_w)

    async def load_dialogs(s):
        i = 0
        async for dialog in s.client.iter_dialogs():
            if i < s.scr_h - 2:
                s.write_chat(i + 1, 2, f"{i} - {dialog.title[:s.chat_max_w - 6]}")
            i += 1
            s.stdscr.refresh()

    async def main(s):
        me = await s.client.get_me()
        s.draw_ui()
        s.write_line(
            0, 1, f"{me.username} -- Chats", len(me.username) + 10, flag=curses.A_BOLD
        )
        try:
            while True:
                if s.stdscr.getch() == ord(" ") and s.stdscr.getch() == ord("q"):
                    s.destroy()
                    break
                await s.load_dialogs()
                s.stdscr.refresh()
        except Exception:
            s.destroy()
            w = traceback.format_exc()
            with open("error.log", "w") as file:
                file.write(w)

    def destroy(s, delay: int = 0):
        curses.nocbreak()
        sleep(delay)
        curses.endwin()

    def run(s):
        try:
            with s.client:
                s.client.loop.run_until_complete(s.main())
        except Exception:
            error_msg = traceback.format_exc()
            with open("error1.log", "w") as efile:
                efile.write(error_msg)
            # s.destroy(10)
