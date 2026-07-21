import curses

from checks.linux.ubuntu_24 import ubuntu_24
from core import ModuleNavigator, ResultViewer, ScanEngine


def main(stdscr: curses.window):
    engine = ScanEngine()

    modules = ModuleNavigator(ubuntu_24).run(stdscr)
    engine.register(*modules)

    results = engine.run(stdscr)
    ResultViewer(results).run(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
