from datetime import date
from pathlib import Path
import grp
import os
import pwd
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


def group_entries() -> list[list[str]]:
    try:
        return [
            line.split(":")
            for line in Path("/etc/group").read_text(errors="ignore").splitlines()
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


def unshadowed_accounts() -> list[str]:
    return [entry[0] for entry in passwd_entries() if len(entry) > 1 and entry[1] != "x"]


def empty_passwords() -> list[str]:
    return [entry[0] for entry in shadow_entries() if len(entry) > 1 and entry[1] == ""]


def missing_primary_groups() -> list[str]:
    group_ids = {entry[2] for entry in group_entries() if len(entry) > 2}
    return [
        f"{entry[0]}:{entry[3]}"
        for entry in passwd_entries()
        if len(entry) > 3 and entry[3] not in group_ids
    ]


def shadow_group_issues() -> list[str]:
    issues: list[str] = []
    shadow_gid = None
    for entry in group_entries():
        if len(entry) > 3 and entry[0] == "shadow":
            shadow_gid = entry[2]
            if entry[3]:
                issues.append("shadow group has members")
            break
    if shadow_gid is not None:
        issues.extend(
            f"{entry[0]} has shadow as primary group"
            for entry in passwd_entries()
            if len(entry) > 3 and entry[3] == shadow_gid
        )
    return issues


def duplicate_accounts(index: int, label: str) -> list[str]:
    entries = passwd_entries() if label in {"UID", "user name"} else group_entries()
    values: dict[str, list[str]] = {}
    for entry in entries:
        if len(entry) > index:
            values.setdefault(entry[index], []).append(entry[0])
    return [
        f"Duplicate {label}: {value} ({', '.join(names)})"
        for value, names in values.items()
        if len(names) > 1
    ]


def interactive_users() -> list[tuple[str, str, int]]:
    shells = valid_shells()
    users: list[tuple[str, str, int]] = []
    for entry in passwd_entries():
        if len(entry) < 7 or entry[6] not in shells or not entry[5]:
            continue
        try:
            gid = int(entry[3])
        except ValueError:
            continue
        users.append((entry[0], entry[5], gid))
    return users


def interactive_home_issues() -> list[str]:
    issues: list[str] = []
    for user, home, _gid in interactive_users():
        path = Path(home)
        if not path.is_dir():
            issues.append(f"{user}: home directory {home} does not exist")
            continue
        try:
            info = path.stat()
            owner = pwd.getpwuid(info.st_uid).pw_name
        except (OSError, KeyError):
            issues.append(f"{user}: home directory {home} cannot be inspected")
            continue
        if owner != user:
            issues.append(f"{user}: home directory {home} is owned by {owner}")
        if info.st_mode & 0o027:
            issues.append(f"{user}: home directory {home} is more permissive than 750")
    return issues


def _home_dot_files(home: Path):
    try:
        root_device = home.stat().st_dev
    except OSError:
        return
    for root, directories, files in os.walk(home, followlinks=False):
        current = Path(root)
        directories[:] = [name for name in directories if not (current / name).is_symlink()]
        try:
            if current.stat().st_dev != root_device:
                directories[:] = []
                continue
        except OSError:
            continue
        for name in files:
            if name.startswith("."):
                path = current / name
                try:
                    if path.is_file() and path.stat().st_dev == root_device:
                        yield path
                except OSError:
                    continue


def interactive_dot_file_issues() -> list[str]:
    issues: list[str] = []
    for user, home, gid in interactive_users():
        try:
            primary_group = grp.getgrgid(gid).gr_name
        except KeyError:
            primary_group = str(gid)
        for path in _home_dot_files(Path(home)):
            name = path.name
            try:
                info = path.stat()
                owner = pwd.getpwuid(info.st_uid).pw_name
                group = grp.getgrgid(info.st_gid).gr_name
            except (OSError, KeyError):
                issues.append(f"{user}: {path} cannot be inspected")
                continue
            if name in {".forward", ".rhost"}:
                issues.append(f"{user}: prohibited file {path} exists")
                continue
            maximum = 0o600 if name in {".bash_history", ".netrc"} else 0o644
            if info.st_mode & 0o777 & ~maximum:
                issues.append(f"{user}: {path} is more permissive than {oct(maximum)}")
            if owner != user:
                issues.append(f"{user}: {path} is owned by {owner}")
            if group != primary_group:
                issues.append(f"{user}: {path} is group-owned by {group}")
    return issues
