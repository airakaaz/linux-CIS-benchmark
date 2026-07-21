import curses
from dataclasses import dataclass


@dataclass(slots=True)
class ScanResult:
    rule_id: str
    title: str
    passed: bool
    message: str
    expected: str | None = None
    found: str | None = None


class ResultViewer:
    COLOR_PASS = 1
    COLOR_FAIL = 2

    def __init__(self, results: list[ScanResult]) -> None:
        self.results = results

        self.expanded: dict[int, bool] = {}

        self.failed_only = False
        self.selected = 0
        self.scroll = 0

        self.active_indices: list[int] = []
        self.failed_indices = [i for i, r in enumerate(self.results) if not r.passed]
        self.all_indices = list(range(len(self.results)))

        self.ID_W = max(len(r.rule_id) for r in results) + 2

    # Initialization

    def _init_curses(self) -> None:
        curses.curs_set(0)
        self.stdscr.keypad(True)

        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(self.COLOR_PASS, curses.COLOR_GREEN, -1)
            curses.init_pair(self.COLOR_FAIL, curses.COLOR_RED, -1)

    # Filtering

    def _update_filter(self) -> None:
        if self.failed_only:
            self.active_indices = self.failed_indices
        else:
            self.active_indices = self.all_indices

        if not self.active_indices:
            self.selected = 0
            self.scroll = 0
            return

        self.selected = max(0, min(self.selected, len(self.active_indices) - 1))
        self._ensure_cursor_visible()

    # Geometry

    def _item_height(self, original_index: int) -> int:
        result = self.results[original_index]

        height = 1

        if self.expanded.get(original_index, False):
            height += 1  # message

            if result.expected is not None:
                height += 1

            if result.found is not None:
                height += 1

        return height

    def _cursor_row(self) -> int:
        row = 0

        for i in range(self.selected):
            row += self._item_height(self.active_indices[i])

        return row

    def _body_height(self) -> int:
        height, _ = self.stdscr.getmaxyx()
        return max(1, height - 6)

    def _ensure_cursor_visible(self) -> None:
        if not self.active_indices:
            self.scroll = 0
            return

        body_height = self._body_height()

        cursor_top = self._cursor_row()
        cursor_bottom = (
            cursor_top + self._item_height(self.active_indices[self.selected]) - 1
        )

        if cursor_top < self.scroll:
            self.scroll = cursor_top

        elif cursor_bottom >= self.scroll + body_height:
            self.scroll = cursor_bottom - body_height + 1

        self.scroll = max(0, self.scroll)

    # Drawing

    def _safe_add(self, y: int, x: int, text: str, attr: int = 0) -> None:
        height, width = self.stdscr.getmaxyx()

        if y < 0 or y >= height:
            return

        if x >= width:
            return

        available = width - x
        if available <= 0:
            return

        try:
            self.stdscr.addnstr(y, x, text, available, attr)
        except curses.error:
            pass

    def _status_attr(self, passed: bool) -> int:
        if not curses.has_colors():
            return curses.A_BOLD

        return (
            curses.color_pair(self.COLOR_PASS if passed else self.COLOR_FAIL)
            | curses.A_BOLD
        )

    def _draw_body(self) -> None:
        body_top = 4
        body_height = self._body_height()

        virtual_row = 0
        screen_row = body_top

        if not self.active_indices:
            self._safe_add(body_top, 0, "No results.")
            return

        for visible_idx, original_idx in enumerate(self.active_indices):
            if screen_row >= body_height + body_top:
                return

            result = self.results[original_idx]

            item_height = self._item_height(original_idx)

            if virtual_row + item_height <= self.scroll:
                virtual_row += item_height
                continue

            self._safe_add(
                screen_row,
                0,
                f" {result.rule_id:<{self.ID_W}}",
                curses.A_BOLD
                | (curses.A_REVERSE if visible_idx == self.selected else 0),
            )
            self._safe_add(
                screen_row,
                self.ID_W,
                f" {result.title[: self.TITLE_W]:<{self.TITLE_W}}",
                curses.A_REVERSE if visible_idx == self.selected else 0,
            )
            self._safe_add(
                screen_row,
                self.ID_W + self.TITLE_W,
                " PASS " if result.passed else " FAIL ",
                self._status_attr(result.passed)
                | (curses.A_REVERSE if visible_idx == self.selected else 0),
            )
            screen_row += 1

            detail_lines: list[str] = []

            if self.expanded.get(original_idx, False):
                detail_lines.append(f"    Message  : {result.message}")

                if result.expected is not None:
                    detail_lines.append(f"    Expected : {result.expected}")

                if result.found is not None:
                    detail_lines.append(f"    Found    : {result.found}")

            _, w = self.stdscr.getmaxyx()
            for line in detail_lines:
                if screen_row >= body_height + body_top:
                    return
                self._safe_add(
                    screen_row,
                    0,
                    f"{line:<{w}}",
                    curses.A_REVERSE if visible_idx == self.selected else 0,
                )
                screen_row += 1

            virtual_row += item_height

    def draw(self) -> None:
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()

        passed = sum(r.passed for r in self.results)
        failed = len(self.results) - passed

        left = f"Passed / Failed / Total : {passed} / {failed} / {len(self.results)}"
        right = "Filter: FAILED ONLY" if self.failed_only else "Filter: ALL"

        self._safe_add(0, 0, left)
        self._safe_add(0, max(0, w - len(right)), right)
        self._safe_add(1, 0, "-" * w)

        self.STATUS_W = 6
        self.TITLE_W = w - self.ID_W - self.STATUS_W  # - 2
        header = (
            f"{'ID':<{self.ID_W}}{'TITLE':^{self.TITLE_W}}{'STATUS':>{self.STATUS_W}}"
        )

        self._safe_add(2, 0, header)
        self._safe_add(3, 0, "-" * w)

        self._draw_body()

        footer = (
            "j/k ↑↓ move | Space expand | "
            f"f/Tab: {'Show All' if self.failed_only else 'Show Failed'} | "
            "q: exit"
        )

        self._safe_add(h - 2, 0, "-" * w)
        self._safe_add(h - 1, 0, f"{footer:^{w}}")

        self.stdscr.refresh()

    # Input

    def _move_up(self) -> None:
        if self.selected > 0:
            self.selected -= 1
            self._ensure_cursor_visible()

    def _move_down(self) -> None:
        if self.selected + 1 < len(self.active_indices):
            self.selected += 1
            self._ensure_cursor_visible()

    def _expand(self) -> None:
        if not self.active_indices:
            return

        idx = self.active_indices[self.selected]

        if not self.expanded.get(idx, False):
            self.expanded[idx] = True
            self._ensure_cursor_visible()

    def _collapse(self) -> None:
        if not self.active_indices:
            return

        idx = self.active_indices[self.selected]

        if self.expanded.get(idx, False):
            self.expanded[idx] = False
            self._ensure_cursor_visible()

    def _toggle_expand(self) -> None:
        if not self.active_indices:
            return

        idx = self.active_indices[self.selected]
        self.expanded[idx] = not self.expanded.get(idx, False)
        self._ensure_cursor_visible()

    def _toggle_filter(self) -> None:
        current_original = None

        if self.active_indices:
            current_original = self.active_indices[self.selected]

        self.failed_only = not self.failed_only
        self._update_filter()

        if current_original is None:
            return

        if current_original in self.active_indices:
            self.selected = self.active_indices.index(current_original)
        else:
            self.selected = min(
                self.selected,
                max(0, len(self.active_indices) - 1),
            )

        self._ensure_cursor_visible()

    def run(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self._init_curses()
        self._update_filter()

        while True:
            self.draw()

            key = self.stdscr.getch()

            if key == curses.KEY_RESIZE:
                self._ensure_cursor_visible()

            elif key in (ord("q"), ord("Q")):
                return

            elif key in (ord("j"), curses.KEY_DOWN):
                self._move_down()

            elif key in (ord("k"), curses.KEY_UP):
                self._move_up()

            elif key in (ord(" "),):
                self._toggle_expand()

            elif key in (ord("l"), curses.KEY_RIGHT):
                self._expand()

            elif key in (ord("h"), curses.KEY_LEFT):
                self._collapse()

            elif key in (ord("f"), ord("F"), 9):
                self._toggle_filter()
