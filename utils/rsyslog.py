from pathlib import Path
import re


CONFIGURATION_FILES = (Path("/etc/rsyslog.conf"), Path("/etc/rsyslog.d"))


def lines() -> list[str]:
    paths: list[Path] = []
    if CONFIGURATION_FILES[0].is_file():
        paths.append(CONFIGURATION_FILES[0])
    try:
        paths.extend(sorted(path for path in CONFIGURATION_FILES[1].glob("*.conf") if path.is_file()))
    except OSError:
        pass
    output: list[str] = []
    for path in paths:
        try:
            output.extend(
                line.split("#", 1)[0].strip()
                for line in path.read_text(errors="ignore").splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            )
        except OSError:
            continue
    return output


def file_create_modes() -> list[int]:
    values: list[int] = []
    pattern = re.compile(r"^\s*\$FileCreateMode\s+([0-7]{3,4})\b", re.IGNORECASE)
    for line in lines():
        match = pattern.match(line)
        if match:
            try:
                values.append(int(match.group(1), 8))
            except ValueError:
                pass
    return values


def receives_remote_logs() -> list[str]:
    patterns = (
        r'^\s*module\(\s*load\s*=\s*"?imtcp"?',
        r'^\s*input\(\s*type\s*=\s*"?imtcp"?\b',
        r'^\s*\$ModLoad\s+imtcp\b',
        r'^\s*\$InputTCPServerRun\b',
    )
    return [line for line in lines() if any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns)]


def gtls_forwarding() -> list[str]:
    pattern = re.compile(r'^\s*StreamDriver\s*=\s*"?gtls"?\b', re.IGNORECASE)
    return [line for line in lines() if pattern.search(line)]
