from dataclasses import dataclass
from pathlib import Path
import re
import shlex

from utils.command import run


AUDIT_RULES_DIRECTORY = Path("/etc/audit/rules.d")
AUDITD_CONFIG = Path("/etc/audit/auditd.conf")


@dataclass(frozen=True, slots=True)
class AuditRuleState:
    running: bool
    persistent: bool

    @property
    def valid(self) -> bool:
        return self.running and self.persistent


def running_auditctl_matches(pattern: str) -> bool:
    result = run("auditctl -l")
    if not result.ok:
        return False

    return re.search(pattern, result.stdout, flags=re.MULTILINE) is not None


def persistent_rules_match(
    pattern: str, directory: Path = AUDIT_RULES_DIRECTORY
) -> bool:
    regex = re.compile(pattern, flags=re.MULTILINE)

    try:
        # The CIS audit uses `grep -qr`, so include every regular file
        # recursively rather than only top-level *.rules files.
        files = sorted(path for path in directory.rglob("*") if path.is_file())
    except OSError:
        return False

    for file in files:
        try:
            content = file.read_text(errors="ignore")
        except OSError:
            continue

        if regex.search(content):
            return True

    return False


def audit_rule_state(
    pattern: str, directory: Path = AUDIT_RULES_DIRECTORY
) -> AuditRuleState:
    return AuditRuleState(
        running=running_auditctl_matches(pattern),
        persistent=persistent_rules_match(pattern, directory=directory),
    )


def auditd_option(option: str, path: Path = AUDITD_CONFIG) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(option)}\s*=\s*(\S+)")
    try:
        for line in path.read_text(errors="ignore").splitlines():
            match = pattern.match(line)
            if match:
                return match.group(1)
    except OSError:
        pass
    return None


def login_uid_min() -> int | None:
    pattern = re.compile(r"^\s*UID_MIN\s+(\d+)")
    try:
        for line in Path("/etc/login.defs").read_text(errors="ignore").splitlines():
            match = pattern.match(line)
            if match:
                return int(match.group(1))
    except (OSError, ValueError):
        pass
    return None


def privileged_files() -> list[Path]:
    from utils.command import run

    # Match the CIS audit's `findmnt -it ...` filter.  Filesystems listed as
    # `nodev` in /proc/filesystems are not real storage filesystems and must
    # not be searched for privileged executables.
    nodev_filesystems: set[str] = set()
    try:
        for line in Path("/proc/filesystems").read_text(errors="ignore").splitlines():
            fields = line.split()
            if len(fields) >= 2 and fields[0] == "nodev":
                nodev_filesystems.add(fields[1])
    except OSError:
        return []

    result = run("findmnt -n -l -k -o TARGET,FSTYPE,OPTIONS")
    if not result.ok:
        return []

    files: list[Path] = []
    for line in result.stdout.splitlines():
        fields = line.split(None, 2)
        if len(fields) != 3:
            continue
        mountpoint, filesystem_type, options = fields
        if filesystem_type in nodev_filesystems:
            continue
        if "noexec" in options or "nosuid" in options:
            continue
        found = run(
            f"find {shlex.quote(mountpoint)} -xdev -perm /6000 -type f -print"
        )
        files.extend(Path(path) for path in found.stdout.splitlines() if path)
    return sorted(set(files))
