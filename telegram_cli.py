import curses


def main():
    # INIT
    stdscr = curses.initscr()
    curses.cbreak()  # Disable line buffering
    stdscr.keypad(True)  # Enables special keys detection

    # Get screen dimenstions
    height, width = stdscr.getmaxyx()

    chat_width = width // 4
    messages_width = width - chat_width - 1

    stdscr.addstr(0, 1, "Chats", curses.A_BOLD)
    chat_list = ["Chat 1", "Chat 2", "Chat 3", "Chat 4"]

    for i, chat in enumerate(chat_list):
        stdscr.addstr(i + 1, 2, f"- {chat}")

    stdscr.vline(0, chat_width, curses.ACS_VLINE, height)

    stdscr.addstr(1, chat_width + 2, "Selected Chat Messages", curses.A_BOLD)
    stdscr.addstr(3, chat_width + 2, "(No message selected yet)")

    selected_chat_index = 0

    stdscr.refresh()

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


if __name__ == "__main__":
    main()
