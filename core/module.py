import curses
from typing import Type

from core.rule import CISRule


class Module:
    def __init__(
        self,
        name: str,
        subMods: list[Module] | None = None,
        rules: list[Type[CISRule]] | None = None,
    ):
        self.name = name
        self._subModules = subMods if subMods else []
        self._rules = rules if rules else []

    @property
    def rules(self) -> list[Type[CISRule]]:
        r = self._rules.copy()
        for mod in self._subModules:
            r.extend(mod.rules)
        return r

    @property
    def subModules(self) -> list[Module]:
        return self._subModules.copy()


def _descendants(module: Module):
    for child in module.subModules:
        yield child
        yield from _descendants(child)


class ModuleNavigator:
    def __init__(self, root: Module):
        self.root = root
        self.cursor = 0
        self.scroll = 0
        self.expanded = set()
        self.selected = set()
        self.maxwidth = 0
        self.hoffset = 0

        self.parent: dict[Module, Module | None] = {}
        self.maxwidth: int = 0

        def build(module: Module, parent: Module | None, d: int):
            self.maxwidth = max(self.maxwidth, 2 * d + len(module.name) + 5)
            self.parent[module] = parent
            for child in module.subModules:
                build(child, module, d + 1)

        build(root, None, 0)

    def _visible(self) -> list[tuple[Module, int]]:
        out = []

        def walk(m, d):
            out.append((m, d))
            if m in self.expanded:
                for s in m.subModules:
                    walk(s, d + 1)

        walk(self.root, 0)
        return out

    def _ordered_selected(self):
        out = []

        def walk(m):
            if m in self.selected:
                out.append(m)
            for s in m.subModules:
                walk(s)

        walk(self.root)
        return out

    def _draw(self, stdscr: curses.window, vis):
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        body = h - 4
        footer = body + 1

        if self.cursor < self.scroll:
            self.scroll = self.cursor
        elif self.cursor >= self.scroll + body:
            self.scroll = self.cursor - body + 1

        self.hoffset = min(5, max(1, body - len(vis)))
        for row, i in enumerate(range(self.scroll, min(len(vis), self.scroll + body))):
            mod, depth = vis[i]
            # 󰛀 󰛂 󰝤 󰁅 󰁔
            if mod in self.selected:
                if mod in self.expanded:
                    mark = ""
                else:
                    mark = "" if mod.subModules else ""
            else:
                if mod in self.expanded:
                    mark = ""
                else:
                    mark = "" if mod.subModules else " "

            line = f" {'  ' * depth} {mark} {mod.name}"
            menu_offset = (w - self.maxwidth) // 2
            stdscr.addnstr(
                row + self.hoffset,
                menu_offset,
                line.ljust(self.maxwidth),
                w - menu_offset - 1,
                curses.A_REVERSE if i == self.cursor else 0,
            )

        stdscr.addnstr(footer + 1, 0, "-" * w, w)
        help = "j/k ↑↓ move  |  h/l ←→ collapse/expand  |  Space: select  |  Enter: confirm  |  q: exit"
        help_offset = max(0, w // 2 - len(help) // 2)
        stdscr.addnstr(footer + 2, help_offset, help, w - help_offset - 1)

        stdscr.refresh()

    def _select(self, module: Module):
        self.selected.add(module)

        # descendants don't need to exist anymore
        for child in _descendants(module):
            self.selected.discard(child)

        # ancestors become redundant
        p = self.parent[module]
        while p:
            self.selected.discard(p)
            p = self.parent[p]

        self._compress(module)

    def _compress(self, module: Module):
        parent = self.parent[module]

        while parent:
            if all(child in self.selected for child in parent.subModules):
                for child in parent.subModules:
                    self.selected.remove(child)

                self.selected.add(parent)
                module = parent
                parent = self.parent[parent]
            else:
                break

    def _deselect(self, module: Module):
        self.selected.discard(module)

    def _is_selected(self, module):
        m = module

        while m:
            if m in self.selected:
                return True
            m = self.parent[m]

        return False

    def run(self, stdscr) -> list[Module]:
        curses.curs_set(0)
        stdscr.keypad(True)
        while True:
            vis = self._visible()
            self.cursor = max(0, min(self.cursor, len(vis) - 1))
            self._draw(stdscr, vis)
            k = stdscr.getch()
            if k in (curses.KEY_UP, ord("k")):
                self.cursor = max(0, self.cursor - 1)
            elif k in (curses.KEY_DOWN, ord("j")):
                self.cursor = min(len(vis) - 1, self.cursor + 1)
            elif k in (curses.KEY_RIGHT, ord("l")):
                m, _ = vis[self.cursor]
                if m.subModules:
                    self.expanded.add(m)
            elif k in (curses.KEY_LEFT, ord("h")):
                m, _ = vis[self.cursor]
                self.expanded.discard(m)
            elif k == ord(" "):
                m, _ = vis[self.cursor]
                if m in self.selected:
                    self._deselect(m)
                else:
                    self._select(m)
            elif k in (10, 13, curses.KEY_ENTER) and self.selected:
                return self._ordered_selected()
            elif k == ord("q"):
                exit()
