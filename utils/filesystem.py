from dataclasses import dataclass
from pathlib import Path
from glob import glob
import re


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


@dataclass(slots=True)
class RegexResult:
    found: bool
    locations: list[str]


def contains_regex(paths: list[str], pattern: str, flags=re.MULTILINE) -> RegexResult:
    regex = re.compile(pattern, flags=flags)
    locations: list[str] = []

    for file in paths:
        path = Path(file)
        if not path.is_file():
            continue

        try:
            content = path.read_text(errors="ignore")
        except OSError:
            continue

        if regex.search(content):
            locations.append(file)

    return RegexResult(
        found=bool(locations),
        locations=locations,
    )
