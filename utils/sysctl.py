from dataclasses import dataclass
from pathlib import Path
import re

from utils.command import run


@dataclass(slots=True)
class SysctlSetting:
    value: str | None
    source: Path | None
    # every (file, value) match found, in systemd's effective-precedence order
    # (index 0 = the one systemd-sysctl actually applies)
    all_matches: list[tuple[Path, str]] = []


CONF_FILE_RE = re.compile(r"^\s*#\s*(/\S+\.conf)\s*$")

SYSTEMD_SYSCTL_CANDIDATES = (
    Path("/lib/systemd/systemd-sysctl"),
    Path("/usr/lib/systemd/systemd-sysctl"),
)


def _find_systemd_sysctl() -> Path | None:
    for candidate in SYSTEMD_SYSCTL_CANDIDATES:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved.is_file():
            return resolved
    return None


def get_ufw_sysctl_file() -> Path | None:
    ufw_conf = Path("/etc/default/ufw")
    if not ufw_conf.exists():
        return None
    for line in ufw_conf.read_text().splitlines():
        if line.strip().startswith("IPT_SYSCTL="):
            raw = line.split("=", 1)[1].strip().strip('"')
            if raw:
                path = Path(raw)
                return path if path.is_file() else None
    return None


def get_effective_config_files() -> list[Path]:
    """
    Ask systemd-sysctl itself which config files are in effect and in what
    order, instead of re-implementing directory precedence/masking by hand.

    `systemd-sysctl --cat-config` prints each active file preceded by a
    "# /path/to/file.conf" header line, already resolved for precedence
    (/etc > /run > /usr/local/lib > /usr/lib > /lib) and masking
    (a same-named file higher in that order disables lower ones).

    We read the header lines in reverse (like `tac` in the bash audit) so
    that the first file we return is the one whose value actually wins.
    """
    binary = _find_systemd_sysctl()
    if binary is None:
        return []

    result = run(f"{str(binary)} --cat-config")
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


def get(parameter: str) -> str | None:
    result = run(f"sysctl -n {parameter}")
    if not result.ok:
        return None
    return result.stdout


def get_value_from_file(parameter: str, file: Path) -> str | None:
    """Public helper: last assignment of `parameter` found in `file`, or None."""
    pattern = re.compile(rf"^\s*{re.escape(parameter)}\s*=\s*(\S+)")
    return _last_match_in_file(pattern, file)


def _last_match_in_file(pattern: re.Pattern, file: Path) -> str | None:
    value = None
    try:
        for line in file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = pattern.match(line)
            if match:
                value = match.group(1)
    except OSError:
        pass
    return value


def get_persistent(parameter: str) -> SysctlSetting:
    """
    Resolve the persistent (on-disk) value of `parameter` the same way
    systemd-sysctl would apply it: ask systemd-sysctl for the effective,
    already-precedence-resolved file list, then check each for the last
    matching assignment.

    Note: this deliberately does NOT include UFW's sysctl file, since UFW
    applies it independently of systemd-sysctl. Handle that separately
    via get_ufw_sysctl_file() where the audit's UFW note applies.
    """
    pattern = re.compile(rf"^\s*{re.escape(parameter)}\s*=\s*(\S+)")
    all_matches: list[tuple[Path, str]] = []

    for file in get_effective_config_files():
        value = _last_match_in_file(pattern, file)
        if value is not None:
            all_matches.append((file, value))

    if not all_matches:
        return SysctlSetting(value=None, source=None, all_matches=[])

    effective_file, effective_value = all_matches[0]
    return SysctlSetting(
        value=effective_value, source=effective_file, all_matches=all_matches
    )
