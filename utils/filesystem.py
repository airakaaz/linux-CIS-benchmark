from pathlib import Path


def exists(path: str) -> bool:
    return Path(path).exists()


def read(path: str) -> str:
    return Path(path).read_text()


def read_lines(path: str) -> list[str]:
    return read(path).splitlines()
