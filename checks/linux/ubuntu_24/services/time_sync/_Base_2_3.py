from pathlib import Path
import re

from checks.templates.service_status import EnabledServiceRule
from utils import systemd
from utils.command import run


def chrony_is_active() -> bool:
    result = run("systemctl is-active chrony.service")
    return result.ok and result.stdout.strip() == "active"


def chrony_config_files() -> list[Path]:
    root = Path("/etc/chrony/chrony.conf")
    if not root.is_file():
        return []

    files = [root]
    include_re = re.compile(r"^\s*(?:confdir|sourcedir)\s+(\S+)")

    try:
        lines = root.read_text(errors="ignore").splitlines()
    except OSError:
        return files

    for line in lines:
        match = include_re.match(line)
        if not match:
            continue

        directory = Path(match.group(1))
        if not directory.is_dir():
            continue

        files.extend(sorted(path for path in directory.glob("*") if path.is_file()))

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in files:
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def chrony_servers() -> list[tuple[Path, str]]:
    server_re = re.compile(r"^\s*(server|pool)(?:\s+|:\s+)(\S+)", re.IGNORECASE)
    servers: list[tuple[Path, str]] = []

    for path in chrony_config_files():
        try:
            lines = path.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for line in lines:
            match = server_re.match(line)
            if match:
                servers.append((path, match.group(2)))

    return servers


def timesyncd_options() -> dict[str, tuple[str, Path]]:
    options = ("NTP", "FallbackNTP")
    option_re = {
        option: re.compile(rf"^\s*{option}\b\s*=\s*([^#\n\r]+)", re.IGNORECASE)
        for option in options
    }
    config_files = systemd.effective_config_files(
        "systemd-analyze", "cat-config /etc/systemd/timesyncd.conf"
    )

    if not config_files:
        config_files = [
            path
            for path in (
                Path("/etc/systemd/timesyncd.conf"),
                Path("/usr/lib/systemd/timesyncd.conf"),
            )
            if path.is_file()
        ]

    found: dict[str, tuple[str, Path]] = {}
    for path in config_files:
        try:
            lines = path.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for option in options:
            matches = [match for line in lines if (match := option_re[option].match(line))]
            if matches and option not in found:
                found[option] = (matches[-1].group(1).strip(), path)

    return found
