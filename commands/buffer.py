import curses


def write_line(
    stdscr: curses._CursesWindow,
    y: int,
    x: int,
    buffer: str,
    max_width: int,
    flags=curses.A_NORMAL,
) -> None:
    stdscr.addstr(y, x, " " * max_width)
    stdscr.addstr(y, x, buffer)
