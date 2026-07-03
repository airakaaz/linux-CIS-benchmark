from pathlib import Path
import stat


def mode(path: str) -> int:
    return stat.S_IMODE(Path(path).stat().st_mode)


def owner(path: str) -> int:
    return Path(path).stat().st_uid


def group(path: str) -> int:
    return Path(path).stat().st_gid
