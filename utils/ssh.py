from pathlib import Path
from glob import glob
import ipaddress
import re
import shlex

from utils.command import run


SSHD_CONFIG = Path("/etc/ssh/sshd_config")


def test_config(connection: str | None = None):
    command = "sshd -T"
    if connection:
        command += f" -C {shlex.quote(connection)}"
    return run(command)


def effective_options(connection: str | None = None) -> dict[str, list[str]]:
    result = test_config(connection)
    if not result.ok:
        return {}

    options: dict[str, list[str]] = {}
    for line in result.stdout.splitlines():
        fields = line.split(None, 1)
        if len(fields) != 2:
            continue
        options.setdefault(fields[0].lower(), []).append(fields[1].strip())
    return options


def _include_patterns(path: Path) -> list[str]:
    try:
        lines = path.read_text(errors="ignore").splitlines()
    except OSError:
        return []

    patterns: list[str] = []
    for line in lines:
        line = line.split("#", 1)[0].strip()
        if not line or not line.lower().startswith("include "):
            continue
        try:
            patterns.extend(shlex.split(line.split(None, 1)[1]))
        except ValueError:
            continue
    return patterns


def config_files() -> list[Path]:
    """Return sshd_config and included .conf files, in discovery order."""
    found: list[Path] = []
    pending = [SSHD_CONFIG]
    seen: set[Path] = set()

    while pending:
        path = pending.pop(0)
        try:
            resolved = path.resolve()
        except OSError:
            resolved = path
        if resolved in seen:
            continue
        seen.add(resolved)

        if resolved == SSHD_CONFIG or resolved.suffix == ".conf":
            found.append(resolved)

        base = resolved.parent
        for pattern in _include_patterns(resolved):
            include = Path(pattern)
            if not include.is_absolute():
                include = base / include
            matches = sorted(Path(match) for match in glob(str(include)))
            for match in matches:
                if match.is_file() and (match.suffix == ".conf" or match == SSHD_CONFIG):
                    pending.append(match)

    return found


def _host_key_paths(public: bool) -> list[Path]:
    options = effective_options()
    paths: list[Path] = []
    for value in options.get("hostkey", []):
        path = Path(value + ".pub") if public else Path(value)
        result = run(f"ssh-keygen -lf {shlex.quote(str(path))}")
        if result.ok and path not in paths:
            paths.append(path)
    return paths


def private_host_keys() -> list[Path]:
    return _host_key_paths(public=False)


def public_host_keys() -> list[Path]:
    return _host_key_paths(public=True)


def banner() -> str | None:
    options = effective_options()
    values = options.get("banner", [])
    if not values or values[-1].lower() == "none":
        return None
    return values[-1]


def weak_ciphers(value: str) -> list[str]:
    weak = re.compile(
        r"^(?:3des|blowfish|cast128|aes(?:128|192|256)-cbc|"
        r"arcfour(?:128|256)?|rijndael-cbc@lysator\.liu\.se)$",
        re.IGNORECASE,
    )
    return [cipher for cipher in value.split(",") if weak.fullmatch(cipher)]


def weak_kex_algorithms(value: str) -> list[str]:
    weak = {
        "diffie-hellman-group1-sha1",
        "diffie-hellman-group14-sha1",
        "diffie-hellman-group-exchange-sha1",
    }
    return [algorithm for algorithm in value.split(",") if algorithm in weak]


def weak_macs(value: str) -> list[str]:
    weak = {
        "hmac-md5", "hmac-md5-96", "hmac-ripemd160", "hmac-sha1-96",
        "umac-64@openssh.com", "hmac-md5-etm@openssh.com",
        "hmac-md5-96-etm@openssh.com", "hmac-ripemd160-etm@openssh.com",
        "hmac-sha1-96-etm@openssh.com", "umac-64-etm@openssh.com",
        "umac-128-etm@openssh.com",
    }
    return [mac for mac in value.split(",") if mac in weak]


def openssh_version() -> tuple[int, int] | None:
    result = run("sshd -V")
    match = re.search(r"OpenSSH_(\d+)\.(\d+)", result.stdout + "\n" + result.stderr)
    return (int(match.group(1)), int(match.group(2))) if match else None


def private_listen_addresses(values: list[str]) -> list[str]:
    private: list[str] = []
    for value in values:
        address = value.rsplit(":", 1)[0]
        if value.startswith("[") and "]" in value:
            address = value[1:value.index("]")]
        try:
            parsed = ipaddress.ip_address(address)
        except ValueError:
            continue
        if parsed.is_private and not (parsed.is_loopback or parsed.is_unspecified):
            private.append(value)
    return private
