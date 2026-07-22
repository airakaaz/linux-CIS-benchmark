import curses
from dataclasses import dataclass
from core.module import Module
from core.result import ScanResult
from core.rule import CISRule, Mode


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
        self.stdscr: curses.window = stdscr
        self.rows: list[_Progress] = []
        self.total_rules = 0
        self.done_rules = 0

    def start(self, module: Module, total: int):
        self.rows.append(_Progress(module, total))
        self.redraw()

    def update(self, rule: CISRule):
        p = self.rows[-1]
        p.current += 1
        self.done_rules += 1
        p.rule = f"{rule.rule_id} {rule.title}"
        if p.current >= p.total:
            p.done = True
            p.rule = ""
        self.redraw()

    def redraw(self):
        s = self.stdscr
        h, w = s.getmaxyx()
        s.erase()

        # Top-right overall progress
        overall = f"{self.done_rules}/{self.total_rules}"
        s.addnstr(0, max(0, w - len(overall) - 2), overall, len(overall), curses.A_BOLD)

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
            s.addnstr(
                y,
                name_x,
                p.module.name,
                max(0, w - name_x - 1),
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

                s.addch(
                    y,
                    bar_x + i,
                    " ",
                    curses.A_REVERSE if i < filled else 0,
                )

            # ----- Counter -----

            counter = f"{p.current}/{p.total}"

            counter_x = bar_x + bar_width + 2

            if counter_x < w:
                s.addnstr(
                    y,
                    counter_x,
                    counter,
                    w - counter_x - 1,
                )

            # ----- Rule -----

            rule = p.rule

            rule_x = max(0, (w - len(rule)) // 2)

            if y + 1 < h:
                s.addnstr(
                    y + 1,
                    rule_x,
                    rule,
                    max(0, w - rule_x - 1),
                )

        s.refresh()


class ScanEngine:
    def __init__(self):
        self._modules = []

    def register(self, *modules: Module):
        self._modules.extend(modules)

    def run(self, stdscr: curses.window):
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
