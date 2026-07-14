from pathlib import Path
import grp
import re

from core import CISRule, Mode, ScanResult
from utils import permissions


AUDITD_CONF = Path("/etc/audit/auditd.conf")
AUDIT_TOOLS = tuple(
    Path(path)
    for path in (
        "/sbin/auditctl",
        "/sbin/aureport",
        "/sbin/ausearch",
        "/sbin/autrace",
        "/sbin/auditd",
        "/sbin/augenrules",
    )
)


def audit_log_directory() -> Path | None:
    if not AUDITD_CONF.is_file():
        return None

    log_files: list[str] = []
    try:
        for line in AUDITD_CONF.read_text(errors="ignore").splitlines():
            match = re.match(r"^\s*log_file\s*=\s*(\S+)", line)
            if match:
                log_files.append(match.group(1))
    except OSError:
        return None

    return Path(log_files[-1]).parent if log_files else None


def audit_log_files() -> list[Path]:
    directory = audit_log_directory()
    if directory is None or not directory.is_dir():
        return []
    return sorted(path for path in directory.iterdir() if path.is_file())


def audit_config_files() -> list[Path]:
    root = Path("/etc/audit")
    if not root.is_dir():
        return []
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".conf", ".rules"}
    )


def audit_log_group() -> str | None:
    if not AUDITD_CONF.is_file():
        return None
    try:
        for line in AUDITD_CONF.read_text(errors="ignore").splitlines():
            match = re.match(r"^\s*log_group\s*=\s*(\S+)", line)
            if match:
                return match.group(1)
    except OSError:
        return None
    return None


def group_id(name: str) -> int | None:
    try:
        return grp.getgrnam(name).gr_gid
    except KeyError:
        return None


def check_paths(
    paths: list[Path],
    *,
    max_mode: int | None = None,
    valid_owners: set[int] | None = None,
    valid_groups: set[int] | None = None,
) -> tuple[list[Path], list[Path]]:
    anomalies: list[Path] = []
    missing: list[Path] = []
    valid_owners = {0} if valid_owners is None else valid_owners
    valid_groups = {0} if valid_groups is None else valid_groups

    for path in paths:
        if not path.exists():
            missing.append(path)
            continue

        valid = True
        if max_mode is not None:
            valid = valid and permissions.at_most(permissions.mode(str(path)), max_mode)
        if valid_owners:
            valid = valid and permissions.owner(str(path)) in valid_owners
        if valid_groups:
            valid = valid and permissions.group(str(path)) in valid_groups
        if not valid:
            anomalies.append(path)

    return anomalies, missing


class AuditdAccessRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def build_result(
        self,
        *,
        paths: list[Path],
        expected: str,
        max_mode: int | None = None,
        valid_owners: set[int] | None = None,
        valid_groups: set[int] | None = None,
        missing_is_failure: bool = True,
        precondition_failure: str | None = None,
    ) -> ScanResult:
        anomalies, missing = check_paths(
            paths,
            max_mode=max_mode,
            valid_owners=valid_owners,
            valid_groups=valid_groups,
        )
        passed = (
            precondition_failure is None
            and not anomalies
            and (not missing or not missing_is_failure)
        )
        issues = [
            *([precondition_failure] if precondition_failure else []),
            *(f"{path} has incorrect access" for path in anomalies),
            *(f"{path} is missing" for path in missing if missing_is_failure),
        ]
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="audit paths are correctly configured" if passed else "; ".join(issues),
            expected=expected,
            found=(
                ", ".join(issues)
                if issues
                else ", ".join(str(path) for path in paths) or "none"
            ),
        )
