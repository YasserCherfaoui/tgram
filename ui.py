import curses

from telethon.tl.custom.dialog import Dialog

from shared_data import SharedData
from utils import get_dialog_index


class UI:
    def __init__(self, shared_data: SharedData, client_connected=False) -> None:
        self.stdscr = None
        self.shared_data = shared_data
        if client_connected:
            self.init_curses()

    def init_curses(self):
        self.stdscr = curses.initscr()
        self.scr_h, self.scr_w = self.stdscr.getmaxyx()
        self.chat_max_w = self.scr_w // 4
        self.messages_max_w = self.scr_w - self.chat_max_w - 1
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)

    def chat_has_changed(self, prev_chat):
        pass

    def draw_ui(self):
        if self.stdscr is not None:
            self.stdscr.keypad(True)
            self.stdscr.vline(0, self.chat_max_w, curses.ACS_VLINE, self.scr_h)

    def write_line(self, y: int, x: int, buffer: str, max: int, flag=curses.A_NORMAL):
        if self.stdscr is not None:
            self.stdscr.addstr(y, x, " " * max)
            self.stdscr.addstr(y, x, buffer, flag)

    def write_chat(self, y: int, x: int, dialog: Dialog):
        if (
            self.shared_data.current_dialog is not None
            and self.shared_data.current_dialog.dialog.id == dialog.id
        ):
            self.write_line(
                y,
                x,
                dialog.title[: self.chat_max_w - 6],
                self.chat_max_w - 4,
                flag=curses.A_REVERSE,
            )
        else:
            self.write_line(
                y,
                x,
                dialog.title[: self.chat_max_w - 6],
                self.chat_max_w - 4,
            )

    def dialog_forward(self):
        current_dialog = self.shared_data.current_dialog
        if current_dialog is None:
            self.shared_data.current_dialog = self.shared_data.dialogs_layout[0]
        else:
            i = get_dialog_index(self.shared_data.dialogs_layout, current_dialog)
            self.shared_data.current_dialog = self.shared_data.dialogs_layout[i + 1]
        self.update_ui()

    def update_ui(self):
        # Chats
        for dialog in self.shared_data.dialogs_layout:
            self.write_chat(dialog.position[0], dialog.position[1], dialog.dialog)
            self.refresh()

    def dialog_backward(self):
        current_dialog = self.shared_data.current_dialog
        if current_dialog is None:
            self.shared_data.current_dialog = self.shared_data.dialogs_layout[0]
        else:
            i = get_dialog_index(self.shared_data.dialogs_layout, current_dialog)
            self.shared_data.current_dialog = self.shared_data.dialogs_layout[i - 1]
        self.update_ui()

    def write_message(self, y: int, x: int, message: str):
        self.write_line(y, x, message, self.messages_max_w)

    def refresh(self):
        if self.stdscr is not None:
            self.stdscr.refresh()

    def cleanup(self):
        curses.endwin()
