from utils.command import run
import re


def writable(schema: str, key: str) -> bool | None:
    result = run(f"gsettings writable {schema} {key}")
    if not result.ok:
        return None
    return result.stdout.strip() == "true"


def get(schema: str, key: str) -> str | None:
    result = run(f"gsettings get {schema} {key}")
    if not result.ok:
        return None
    value = result.stdout.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        value = value[1:-1]
    return value
