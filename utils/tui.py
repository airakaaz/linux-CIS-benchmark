import curses
from typing import Callable

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

        if trunc and len(text) >= trunc:
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


class SelectorMenu:
    def __init__(self, title: str, opts: dict):
        self.title = title
        self.opts = opts
        self.names = list(self.opts.keys())

        self.cursor = 0

    def _draw(self):
        self.stdscr.erase()

        h, w = self.stdscr.getmaxyx()

        start_y = h // 2 - (len(self.names) + 1) // 2

        self.scrmgr.write(0, 0, f"{self.title:^{w}}")
        self.scrmgr.h_sep(1)

        for i, name in enumerate(self.names):
            attr = curses.A_REVERSE if i == self.cursor else 0
            self.scrmgr.write(start_y + i, 0, f"{name:^{w}}", attr)

        self.scrmgr.footer("j/k ↑↓ move  |  Enter: pick  |  q/Esc: cancel")

        self.stdscr.refresh()

    def run(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.scrmgr = ScreenManager(stdscr)

        while True:
            self._draw()

            key = self.stdscr.getch()

            if key in (curses.KEY_UP, ord("k")):
                self.cursor -= 1
                if self.cursor < 0:
                    self.cursor = len(self.names) - 1

            elif key in (curses.KEY_DOWN, ord("j")):
                self.cursor += 1
                if self.cursor >= len(self.names):
                    self.cursor = 0

            elif key in (10, 13, curses.KEY_ENTER):
                name = self.names[self.cursor]
                return self.opts[name]

            elif key in (27, ord("q")):
                return None
