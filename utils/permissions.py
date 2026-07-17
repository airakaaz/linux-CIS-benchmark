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


def check_paths(
    paths: list[Path],
    *,
    max_mode: int | None = None,
    valid_owners: set[int] | None = None,
    valid_groups: set[int] | None = None,
) -> tuple[list[Path], list[Path]]:

    anomalies: list[Path] = []
    missing: list[Path] = []

    for path in paths:
        if not path.exists():
            missing.append(path)
            continue

        valid = True
        if max_mode is not None:
            valid = at_most(mode(str(path)), max_mode)
        if valid_owners:
            valid = valid and owner(str(path)) in valid_owners
        if valid_groups:
            valid = valid and group(str(path)) in valid_groups
        if not valid:
            anomalies.append(path)

    return anomalies, missing
