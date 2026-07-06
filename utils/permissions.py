from pathlib import Path
import stat


def mode(path: str) -> int:
    return stat.S_IMODE(Path(path).stat().st_mode)


def owner(path: str) -> int:
    return Path(path).stat().st_uid


def group(path: str) -> int:
    return Path(path).stat().st_gid


def mode_octal(path: str) -> str:
    return f"{mode(path):03o}"


def at_most(actual: int, maximum: int) -> bool:
    for shift in (6, 3, 0):
        actual_bits = (actual >> shift) & 0b111
        max_bits = (maximum >> shift) & 0b111

        if actual_bits | max_bits != max_bits:
            return False

    return True
