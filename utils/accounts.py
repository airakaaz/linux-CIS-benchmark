from datetime import date
from pathlib import Path
import re

from utils.command import run
from utils import permissions


def login_value(name: str) -> str | None:
    try:
        for line in Path("/etc/login.defs").read_text(errors="ignore").splitlines():
            match = re.match(rf"^\s*{re.escape(name)}\s+(\S+)", line)
            if match:
                return match.group(1)
    except OSError:
        pass
    return None


def passwd_entries() -> list[list[str]]:
    try:
        return [
            line.split(":")
            for line in Path("/etc/passwd").read_text(errors="ignore").splitlines()
            if line
        ]
    except OSError:
        return []


def shadow_entries() -> list[list[str]]:
    try:
        return [
            line.split(":")
            for line in Path("/etc/shadow").read_text(errors="ignore").splitlines()
            if line
        ]
    except OSError:
        return []


def password_entries() -> list[list[str]]:
    return [
        entry
        for entry in shadow_entries()
        if len(entry) > 1 and re.match(r"^\$.+\$", entry[1])
    ]


def valid_shells() -> set[str]:
    try:
        return {
            line.strip()
            for line in Path("/etc/shells").read_text(errors="ignore").splitlines()
            if line.strip()
            and not line.lstrip().startswith("#")
            and not line.rstrip().endswith("/nologin")
        }
    except OSError:
        return set()


def uid_min() -> int:
    try:
        return int(login_value("UID_MIN") or "1000")
    except ValueError:
        return 1000


def root_password_status() -> str | None:
    result = run("passwd -S root")
    fields = result.stdout.split()
    return fields[1] if len(fields) > 1 else None


def root_path() -> str | None:
    result = run("sudo -u root env")
    for line in result.stdout.splitlines():
        if line.startswith("PATH="):
            return line.split("=", 1)[1]
    return None


def root_path_issues() -> list[str]:
    value = root_path()
    if value is None:
        return ["root PATH is unavailable"]
    issues: list[str] = []
    if "::" in value:
        issues.append("contains an empty directory")
    if value.endswith(":"):
        issues.append("has a trailing colon")
    for location in value.split(":"):
        if location in {"", "."}:
            continue
        path = Path(location)
        if not path.is_dir():
            issues.append(f"{location} is not a directory")
            continue
        try:
            if permissions.owner(location) != 0:
                issues.append(f"{location} is not root-owned")
            if permissions.mode(location) & 0o022:
                issues.append(f"{location} is group/world writable")
        except OSError:
            issues.append(f"{location} cannot be inspected")
    if re.search(r"(^|:)\.(?:$|:)", value):
        issues.append("contains the current directory")
    return issues


def root_umask_issues() -> list[str]:
    issues: list[str] = []
    for path in (Path("/root/.profile"), Path("/root/.bashrc")):
        try:
            lines = path.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for line in lines:
            match = re.match(r"^\s*umask\s+([0-7]{1,4})\b", line)
            if match:
                value = int(match.group(1), 8)
                if value & 0o027 != 0o027:
                    issues.append(f"{path}: umask {match.group(1)} is too permissive")
    return issues


def system_accounts_with_valid_shell() -> list[str]:
    excluded = {"root", "halt", "sync", "shutdown", "nfsnobody"}
    shells = valid_shells()
    return [
        entry[0]
        for entry in passwd_entries()
        if len(entry) >= 7
        and entry[0] not in excluded
        and (
            int(entry[2]) < uid_min()
            if entry[2].isdigit()
            else False or entry[2] == "65534"
        )
        and entry[6] in shells
    ]


def nonroot_invalid_shells_unlocked() -> list[str]:
    shells = valid_shells()
    users = [
        entry[0]
        for entry in passwd_entries()
        if len(entry) >= 7 and entry[0] != "root" and entry[6] not in shells
    ]
    unlocked: list[str] = []
    for user in users:
        fields = run(f"passwd -S {user}").stdout.split()
        if len(fields) < 2 or fields[1] != "L":
            unlocked.append(user)
    return unlocked


def tmout_issues() -> list[str]:
    paths = [Path("/etc/profile")]
    paths.extend(Path("/etc").glob("*bashrc"))
    paths.extend(Path("/etc/profile.d").glob("*.sh"))
    files = []
    for path in paths:
        try:
            content = path.read_text(errors="ignore")
        except OSError:
            continue
        if re.search(r"\bTMOUT\b", content):
            files.append((path, content))
    if not files:
        return ["TMOUT is not configured"]
    issues: list[str] = []
    for path, content in files:
        values = re.findall(r"^\s*TMOUT\s*=\s*(\d+)\b", content, re.MULTILINE)
        if not values:
            issues.append(f"{path}: TMOUT value missing")
            continue
        if any(int(value) <= 0 or int(value) > 900 for value in values):
            issues.append(f"{path}: TMOUT is outside 1..900")
        if not re.search(
            r"^\s*(?:readonly\s+TMOUT|typeset\s+-xr\s+TMOUT=)", content, re.MULTILINE
        ):
            issues.append(f"{path}: TMOUT is not readonly")
        if not re.search(
            r"^\s*(?:export\s+.*\bTMOUT\b|typeset\s+-xr\s+TMOUT=)",
            content,
            re.MULTILINE,
        ):
            issues.append(f"{path}: TMOUT is not exported")
    return issues


def umask_issues() -> list[str]:
    issues: list[str] = []
    profile_values: list[int] = []
    for path in Path("/etc/profile.d").glob("*.sh"):
        try:
            profile_values.extend(
                int(value, 8)
                for value in re.findall(
                    r"^\s*umask\s+([0-7]{1,4})\b",
                    path.read_text(errors="ignore"),
                    re.MULTILINE,
                )
            )
        except OSError:
            continue
    login = login_value("UMASK")
    if not profile_values:
        issues.append("no profile.d umask is configured")
    if login is None:
        issues.append("UMASK is not configured in /etc/login.defs")
    values = profile_values + (
        [int(login, 8)] if login and re.fullmatch(r"[0-7]+", login) else []
    )
    if any(value & 0o027 != 0o027 for value in values):
        issues.append("umask is less restrictive than 027")
    return issues


def future_password_changes() -> list[str]:
    today = date.today().toordinal() - date(1970, 1, 1).toordinal()
    return [
        entry[0]
        for entry in password_entries()
        if len(entry) > 2 and entry[2].isdigit() and int(entry[2]) > today
    ]
