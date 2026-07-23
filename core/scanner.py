from typing import Callable, Type
import curses
from dataclasses import dataclass
from enum import Enum
from core.module import Module
from core.result import ScanResult
from core.rule import CISRule, Mode
from utils import tui


@dataclass
class _Progress:
    module: Module
    total: int
    current: int = 0
    rule: str = ""
    done: bool = False


class ScanScreen:
    BAR_WIDTH = 40

    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.scr_mgr = tui.ScreenManager(stdscr)
        self.scr_mgr.init_curses()

        self.rows: list[_Progress] = []
        self.total_rules = 0
        self.done_rules = 0

    def start(self, module: Module, total: int):
        self.rows.append(_Progress(module, total))
        self.redraw()

    def update(self, rule: Type[CISRule]):
        p = self.rows[-1]
        p.current += 1
        self.done_rules += 1
        p.rule = f"{rule.rule_id} {rule.title}"
        if p.current >= p.total:
            p.done = True
            p.rule = ""
        self.redraw()

    def redraw(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.erase()

        # Top-right overall progress
        overall = f"{self.done_rules}/{self.total_rules}"
        self.scr_mgr.write(0, max(0, w - len(overall) - 2), overall, curses.A_BOLD)

        row_height = 3

        active = max(0, len(self.rows) - 1)

        visible_rows = max(1, (h - 2) // row_height)

        first = max(0, active - visible_rows // 2)
        first = min(first, max(0, len(self.rows) - visible_rows))

        start_y = max(2, (h - min(len(self.rows), visible_rows) * row_height) // 2)

        bar_width = min(self.BAR_WIDTH, max(10, w - 40))
        bar_x = max(0, (w - bar_width) // 2)

        for screen_row, p in enumerate(self.rows[first : first + visible_rows]):
            y = start_y + screen_row * row_height

            if y + 1 >= h:
                break

            # ----- Module Name -----
            name_x = max(0, bar_x - len(p.module.name) - 3)
            self.scr_mgr.write(
                y,
                name_x,
                p.module.name,
                curses.A_BOLD,
            )

            # ----- Progress bar -----
            filled = (
                bar_width
                if p.done
                else (0 if p.total == 0 else p.current * bar_width // p.total)
            )

            for i in range(bar_width):
                if bar_x + i >= w:
                    break

                self.scr_mgr.write(
                    y,
                    bar_x + i,
                    " ",
                    curses.A_REVERSE if i < filled else 0,
                )

            # ----- Counter -----

            counter = f"{p.current}/{p.total}"

            counter_x = bar_x + bar_width + 2

            if counter_x < w:
                self.scr_mgr.write(
                    y,
                    counter_x,
                    counter,
                )

            # ----- Rule -----

            rule = p.rule

            rule_x = max(0, (w - len(rule)) // 2)

            if y + 1 < h:
                self.scr_mgr.write(
                    y + 1,
                    rule_x,
                    rule,
                )

        self.stdscr.refresh()


class ScanEngine:
    def __init__(self):
        self._modules: list[Module] = []

    def register(self, *modules: Module):
        self._modules.extend(modules)

    def run(self, stdscr: curses.window, filter: Callable, lvl: Enum):
        self._modules = filter(self._modules, lvl)
        results: list[ScanResult] = []
        screen = ScanScreen(stdscr)
        screen.total_rules = sum(len(m.rules) for m in self._modules)

        for mod in self._modules:
            screen.start(mod, len(mod.rules))
            for rule in mod.rules:
                if rule.mode == Mode.AUTOMATIC:
                    try:
                        results.append(rule().check())
                    except Exception as e:
                        results.append(
                            ScanResult(
                                rule_id=rule.rule_id,
                                title=rule.title,
                                passed=False,
                                message=f"check failed due to Exception: {e}",
                            )
                        )
                    screen.update(rule)
        return results
