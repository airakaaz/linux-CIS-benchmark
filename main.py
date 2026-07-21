import curses
import os
import sys

from checks.linux.ubuntu_24 import ubuntu_24
from core import ModuleNavigator, ResultViewer, ScanEngine


def main(stdscr: curses.window):
    engine = ScanEngine()

    modules = ModuleNavigator(ubuntu_24).run(stdscr)
    engine.register(*modules)

    results = engine.run(stdscr)
    ResultViewer(results).run(stdscr)


if __name__ == "__main__":
    if os.geteuid() == 0:
        curses.wrapper(main)
    else:
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
