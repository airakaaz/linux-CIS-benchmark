from pathlib import Path
from glob import glob


def exists(path: str) -> bool:
    return Path(path).exists()


def read(path: str) -> str:
    return Path(path).read_text()


def read_lines(path: str) -> list[str]:
    return read(path).splitlines()


def resolve_paths(*patterns: str) -> list[str]:
    paths = []

    for pattern in patterns:
        paths.extend(sorted(glob(pattern)))

    return paths
