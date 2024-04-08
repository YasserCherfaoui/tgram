from asyncio.tasks import sleep
import curses
from commands.buffer import write_line
from telethon import TelegramClient
from telethon.client.updates import traceback


async def main(client: TelegramClient):
    try:
        # INIT
        stdscr = curses.initscr()
        curses.cbreak()  # Disable line buffering
        stdscr.keypad(True)  # Enables special keys detection
        curses.noecho()
        curses.curs_set(0)
        # curses.cbreak()

        me = await client.get_me()
        # Get screen dimenstions
        height, width = stdscr.getmaxyx()

        chat_width = width // 4
        messages_width = width - chat_width - 1

        stdscr.addstr(0, 1, f"{me.username} -- Chats", curses.A_BOLD)

        stdscr.vline(0, chat_width, curses.ACS_VLINE, height)

        stdscr.addstr(1, chat_width + 2, "Selected Chat Messages", curses.A_BOLD)
        stdscr.addstr(3, chat_width + 2, "(No message selected yet)")

        selected_chat_index = 0

        stdscr.refresh()
        while True:
            dialogs_iter = client.iter_dialogs()
            key = stdscr.getch()
            if key == ord(" ") and stdscr.getch() == ord("q"):
                await kill_curses(0)
                break

            i = 0
            stdscr.refresh()
            async for dialog in dialogs_iter:
                if i < height - 4:
                    stdscr.addstr(i + 1, 2, " " * (chat_width - 2))
                    stdscr.addstr(i + 1, 2, f"{i}- {dialog.title[:chat_width-6]}")
                    write_line(
                        stdscr,
                        i + 1,
                        2,
                        f"{i} - {dialog.title[:chat_width - 6]}",
                        chat_width - 2,
                    )
                i += 1
                stdscr.refresh()

    except Exception:
        error = traceback.format_exc()
        with open("error.log", "w") as error_file:
            error_file.write(error)
        await kill_curses()


async def kill_curses(delay: float = 2):
    curses.nocbreak()
    await sleep(delay)
    curses.endwin()


""""
    while True:
        key = stdscr.getch()
        prev_index = selected_chat_index
        if key == curses.KEY_UP and selected_chat_index > 0:
            selected_chat_index -= 1
        elif key == curses.KEY_DOWN and selected_chat_index < len(chat_list) - 1:
            selected_chat_index += 1

        stdscr.addstr(
            prev_index + 1,
            2,
            " " * len(chat_list[selected_chat_index]),
            curses.A_NORMAL,
        )
        stdscr.addstr(prev_index + 1, 2, f"- {chat_list[prev_index]}")
        stdscr.addstr(
            selected_chat_index + 1,
            2,
            f"- {chat_list[selected_chat_index]}",
            curses.A_REVERSE,
        )
        stdscr.refresh()
        if key == curses.KEY_EXIT:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.endwin()
            exit()

"""

if __name__ == "__main__":
    print("Run start.py instead i.e:\n$ python3 start.py")
