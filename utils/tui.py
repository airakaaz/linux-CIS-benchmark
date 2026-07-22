import curses

h_sep = "─"


class ScreenManager:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr

    def init_curses(self) -> None:
        curses.curs_set(0)
        self.stdscr.keypad(True)

        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()

    def write(
        self, y: int, x: int, text: str, attr: int = 0, trunc: int | None = None
    ) -> None:
        height, width = self.stdscr.getmaxyx()

        if y < 0 or y >= height:
            return

        if x >= width:
            return

        available = width - x
        if available <= 0:
            return

        if trunc:
            text = text[: trunc - 1] + "…"

        try:
            self.stdscr.addnstr(y, x, text, available, attr)
        except curses.error:
            pass

    def footer(self, footer: str):
        h, w = self.stdscr.getmaxyx()
        self.h_sep(h - 2)
        self.write(h - 1, 0, f"{footer:^{w}}")

    def h_sep(self, h: int, *, sep=h_sep):
        _, w = self.stdscr.getmaxyx()
        self.write(h, 0, sep * w)
