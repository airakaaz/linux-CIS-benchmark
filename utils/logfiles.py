from pathlib import Path
import grp
import pwd
import re

from utils import accounts, permissions


def _allowed_owner(name: str, allowed: set[str]) -> bool:
    return name in allowed


def _policy(path: Path, owner: str, group: str) -> tuple[int, set[str], set[str]]:
    basename = path.name
    if path.parent.name == "apt":
        return 0o640, {"root"}, {"root", "adm"}
    if re.match(r"^(?:lastlog(?:\..*)?|wtmp(?:\..*)?|wtmp-.*|btmp(?:\..*)?|btmp-.*|README)$", basename):
        return 0o664, {"root"}, {"root", "utmp"}
    if re.match(r"^(?:cloud-init\.log.*|localmessages.*|waagent\.log.*)$", basename):
        return 0o644, {"root", "syslog"}, {"root", "adm"}
    if basename in {"auth.log", "syslog", "messages"} or re.match(r"^(?:secure|secure,.*|secure-.*)$", basename):
        return 0o640, {"root", "syslog"}, {"root", "adm"}
    if basename in {"SSSD", "sssd"}:
        return 0o660, {"root", "SSSD"}, {"root", "SSSD"}
    if basename in {"gdm", "gdm3"}:
        return 0o660, {"root"}, {"root", "gdm", "gdm3"}
    if basename.endswith(".journal") or basename.endswith(".journal~"):
        return 0o640, {"root"}, {"root", "systemd-journal"}

    owners = {"root", "syslog"}
    groups = {"root", "adm"}
    try:
        shell = next(entry[6] for entry in accounts.passwd_entries() if entry[0] == owner and len(entry) >= 7)
    except StopIteration:
        shell = ""
    if owner != "root" and shell not in accounts.valid_shells():
        owners.add(owner)
        groups.add(group)
    return 0o640, owners, groups


def permission_issues() -> list[str]:
    issues: list[str] = []
    root = Path("/var/log")
    if not root.is_dir():
        return ["/var/log does not exist"]
    try:
        paths = [path for path in root.rglob("*") if path.is_file()]
    except OSError:
        return ["/var/log could not be inspected"]
    for path in paths:
        try:
            info = path.stat()
            owner = pwd.getpwuid(info.st_uid).pw_name
            group = grp.getgrgid(info.st_gid).gr_name
        except (OSError, KeyError):
            issues.append(f"{path} cannot be inspected")
            continue
        maximum, owners, groups = _policy(path, owner, group)
        if not permissions.at_most(permissions.mode(str(path)), maximum):
            issues.append(f"{path}: mode is more permissive than {oct(maximum)}")
        if not _allowed_owner(owner, owners):
            issues.append(f"{path}: owner {owner} is not one of {sorted(owners)}")
        if group not in groups:
            issues.append(f"{path}: group {group} is not one of {sorted(groups)}")
    return issues
