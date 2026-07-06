import glob
import re
from pathlib import Path

from utils.command import run


_SYSCTL_GLOBS = [
    "/etc/sysctl.d/*.conf",
    "/run/sysctl.d/*.conf",
    "/usr/local/lib/sysctl.d/*.conf",
    "/usr/lib/sysctl.d/*.conf",
    "/lib/sysctl.d/*.conf",
]
_SYSCTL_MAIN_FILE = "/etc/sysctl.conf"
_UFW_DEFAULTS_FILE = "/etc/default/ufw"


def get_runtime_value(parameter: str) -> str | None:
    result = run(f"sysctl -n {parameter}")
    return result.stdout.strip() if result.ok else None


def _extract_value(content: str, parameter: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(parameter)}\s*=\s*(\S+)", re.MULTILINE)
    matches = pattern.findall(content)
    return (
        matches[-1] if matches else None
    )  # last match wins, per systemd-sysctl precedence


def get_configured_values(parameter: str) -> dict[str, str]:
    found: dict[str, str] = {}

    candidates = [_SYSCTL_MAIN_FILE]
    for pattern in _SYSCTL_GLOBS:
        candidates.extend(sorted(glob.glob(pattern)))

    for path in candidates:
        file = Path(path)
        if not file.is_file():
            continue
        value = _extract_value(file.read_text(errors="ignore"), parameter)
        if value is not None:
            found[path] = value

    ufw_file = Path(_UFW_DEFAULTS_FILE)
    if ufw_file.is_file():
        match = re.search(
            r"^\s*IPT_SYSCTL\s*=\s*(\S+)",
            ufw_file.read_text(errors="ignore"),
            re.MULTILINE,
        )
        if match:
            ufw_sysctl_file = Path(match.group(1).strip("\"'"))
            if ufw_sysctl_file.is_file():
                value = _extract_value(
                    ufw_sysctl_file.read_text(errors="ignore"), parameter
                )
                if value is not None:
                    found[str(ufw_sysctl_file)] = value

    return found
