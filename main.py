import curses
import os
import sys

from checks.linux.ubuntu_24 import ubuntu_24
from core import ModuleNavigator, ResultViewer, ScanEngine, Module
from utils import tui

ACTIFS: dict[str, Module] = {"ubuntu 24.04": ubuntu_24}


def main(stdscr: curses.window):
    engine = ScanEngine()

    actif = tui.SelectorMenu("Choose Actif", ACTIFS).run(stdscr)
    if not actif:
        return

    lvl = tui.SelectorMenu("Choose level", actif.levels).run(stdscr)
    if not lvl:
        return

    modules = ModuleNavigator(actif).run(stdscr)

    engine.register(*modules)

    results = engine.run(stdscr, actif.filter, lvl)
    ResultViewer(results).run(stdscr)


if __name__ == "__main__":
    if os.geteuid() == 0:
        curses.wrapper(main)
    else:
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
