from dataclasses import dataclass
from pathlib import Path
import re

from utils.command import run

SYSTEMD_BINARY_CANDIDATES = (
    Path("/lib/systemd/"),
    Path("/usr/lib/systemd/"),
)

CONF_FILE_RE = re.compile(r"^\s*#\s*(/\S+\.conf)\s*$")
SECTION_HEADER_RE = re.compile(r"^\s*\[([^\]]+)\]\s*$")


def _find_systemd_binary(binary: str) -> Path | None:
    for candidate in SYSTEMD_BINARY_CANDIDATES:
        candidate = candidate / binary
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved.is_file():
            return resolved
    return None


def effective_config_files(binary_name: str, command_opt: str) -> list[Path]:
    binary = _find_systemd_binary(binary_name)
    if binary is None:
        return []

    result = run(str(binary) + " " + command_opt)
    if not result.ok:
        return []

    files: list[Path] = []
    seen: set[str] = set()
    for line in reversed(result.stdout.splitlines()):
        match = CONF_FILE_RE.match(line)
        if not match:
            continue
        candidate = Path(match.group(1))
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        key = str(resolved)
        if key not in seen and resolved.is_file():
            seen.add(key)
            files.append(resolved)
    return files


@dataclass(slots=True)
class SystemdConfSetting:
    value: str | None
    source: Path | None
    is_default: bool = False  # True if pulled from the fallback/default branch


def _section_lines(content: str, section: str) -> list[str]:
    lines: list[str] = []
    in_section = False
    for line in content.splitlines():
        header = SECTION_HEADER_RE.match(line)
        if header:
            in_section = header.group(1).strip().lower() == section.lower()
            continue
        if in_section:
            lines.append(line)
    return lines


def _match_option(
    lines: list[str], option: str, allow_commented: bool = False
) -> str | None:
    """Last matching assignment of `option` within the given lines."""
    if allow_commented:
        pattern = re.compile(
            rf"^(?:\s*#)?\s*{re.escape(option)}\s*=\s*(?P<value>\S+)",
            re.IGNORECASE,
        )
    else:
        pattern = re.compile(
            rf"^\s*{re.escape(option)}\s*=\s*(?P<value>\S+)", re.IGNORECASE
        )

    value = None
    for line in lines:
        match = pattern.match(line)
        if match:
            value = match.group("value")
    return value


def get_option(conf_unit: str, section: str, option: str) -> SystemdConfSetting:
    for file in effective_config_files("systemd-analyze", "cat-config " + conf_unit):
        content = file.read_text(errors="ignore")
        lines = _section_lines(content, section)
        value = _match_option(lines, option, allow_commented=False)
        if value is not None:
            return SystemdConfSetting(value=value, source=file, is_default=False)

    for base in (Path("/etc") / conf_unit, Path("/usr/lib") / conf_unit):
        try:
            resolved = base.resolve()
        except OSError:
            continue
        if not resolved.is_file():
            continue
        content = resolved.read_text(errors="ignore")
        lines = _section_lines(content, section)
        value = _match_option(lines, option, allow_commented=True)
        if value is not None:
            return SystemdConfSetting(value=value, source=resolved, is_default=True)

    return SystemdConfSetting(value=None, source=None, is_default=False)
