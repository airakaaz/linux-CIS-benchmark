from pathlib import Path
import re

from utils.command import run


SUDOERS = Path("/etc/sudoers")
SUDOERS_DIRECTORY = Path("/etc/sudoers.d")


def files() -> list[Path]:
    found = [SUDOERS]
    try:
        if SUDOERS_DIRECTORY.is_dir():
            found.extend(path for path in SUDOERS_DIRECTORY.rglob("*") if path.is_file())
    except OSError:
        pass
    return found


def lines() -> list[str]:
    output: list[str] = []
    for path in files():
        try:
            output.extend(path.read_text(errors="ignore").splitlines())
        except OSError:
            continue
    return output


def active_lines(pattern: str) -> list[str]:
    regex = re.compile(pattern, re.IGNORECASE)
    return [line for line in lines() if not line.lstrip().startswith("#") and regex.search(line)]


def logfile() -> str | None:
    pattern = re.compile(r"^\s*Defaults\s+.*?\blogfile\s*=\s*[\"']?([^\"'\s,]+)", re.IGNORECASE)
    value = None
    for line in lines():
        if line.lstrip().startswith("#"):
            continue
        match = pattern.search(line)
        if match:
            value = match.group(1)
    return value


def timestamp_values() -> list[float]:
    values: list[float] = []
    pattern = re.compile(r"timestamp_timeout\s*=\s*(-?\d+(?:\.\d+)?)", re.IGNORECASE)
    for line in lines():
        if line.lstrip().startswith("#"):
            continue
        for match in pattern.finditer(line):
            values.append(float(match.group(1)))
    return values


def default_timestamp_timeout() -> float | None:
    result = run("sudo -V")
    match = re.search(
        r"Authentication timestamp timeout:\s*(-?\d+(?:\.\d+)?)\s+minutes",
        result.stdout,
        re.IGNORECASE,
    )
    return float(match.group(1)) if match else None
