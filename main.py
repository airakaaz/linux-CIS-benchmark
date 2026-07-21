import curses

from checks.linux.ubuntu_24 import ubuntu_24
from core import ScanEngine
from core import ModuleNavigator


def main(stdscr: curses.window):
    engine = ScanEngine()
    print("hello")
    modules = ModuleNavigator(ubuntu_24).run(stdscr)
    print("hello")
    engine.register(*modules)
    print("hello")

    results = engine.run()
    # return results

    # --------------------------------------------------------
    total = len(results)
    passed = 0

    for result in results:
        if result.passed:
            passed += 1

        print("id       :", result.rule_id)
        print("title    :", result.title)
        print("expected :", result.expected)
        print("found    :", result.found)
        print("passed   :", result.passed)
        print("message  :", result.message)
        print()

    print("=============")
    print(f"score    : {passed}/{total}")


if __name__ == "__main__":
    curses.wrapper(main)
    # print(curses.wrapper(main))
