from pathlib import Path
import re

from core import CISRule, Mode, ScanResult
from utils import audit


def watch(path: str, key: str) -> str:
    return (
        rf"(?=.*(?:^|\s)-w\s+{re.escape(path)}(?=\s|$))"
        rf"(?=.*-p\s+wa\b)"
        rf"(?=.*(?:-k\s+|key=){re.escape(key)}\b)"
    )


class AuditRuleSetRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC
    _PATTERNS: tuple[str, ...] = ()

    def check(self) -> ScanResult:
        states = [audit.audit_rule_state(pattern) for pattern in self._PATTERNS]
        passed = bool(states) and all(state.valid for state in states)
        failed = [
            f"requirement {index + 1}: running={state.running}, persistent={state.persistent}"
            for index, state in enumerate(states)
            if not state.valid
        ]
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "audit rules are present in running and persistent configuration"
                if passed
                else "audit rule requirements are missing: " + "; ".join(failed)
            ),
            expected=f"{len(self._PATTERNS)} audit rule requirements in running and persistent configuration",
            found="all requirements present" if passed else "; ".join(failed),
        )


def executable(path: str, key: str) -> str:
    return (
        rf"(?=.*(?:-F\s+)?path={re.escape(path)}(?=\s|$))"
        rf"(?=.*(?:-F\s+)?perm=x\b)"
        rf"(?=.*auid>=\d+)"
        rf"(?=.*auid!=(?:unset|-1|4294967295))"
        rf"(?=.*(?:-k\s+|key=){re.escape(key)}\b)"
    )


def sudo_log_file() -> str | None:
    files = [Path("/etc/sudoers")]
    directory = Path("/etc/sudoers.d")
    try:
        if directory.is_dir():
            files.extend(sorted(path for path in directory.iterdir() if path.is_file()))
    except OSError:
        pass

    pattern = re.compile(r"^\s*Defaults\s+.*?\blogfile\s*=\s*[\"']?([^\"'\s,]+)", re.IGNORECASE)
    found: str | None = None
    for path in files:
        try:
            for line in path.read_text(errors="ignore").splitlines():
                match = pattern.match(line)
                if match:
                    found = match.group(1)
        except OSError:
            continue
    return found


class SudoLogRule(CISRule):
    rule_id = "6.2.3.3"
    title = "Ensure events that modify the sudo log file are collected"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        path = sudo_log_file()
        state = audit.audit_rule_state(watch(path, "sudo_log_file")) if path else None
        passed = state is not None and state.valid
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "sudo logfile is configured and audited"
                if passed
                else "sudo logfile is not configured or is not audited"
            ),
            expected="sudo logfile exists and is watched with key sudo_log_file in both configurations",
            found=(
                f"{path}: running={state.running}, persistent={state.persistent}"
                if state is not None
                else "sudo logfile not configured"
            ),
        )


class PrivilegedCommandRule(CISRule):
    rule_id = "6.2.3.10"
    title = "Ensure use of privileged commands are collected"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        paths = audit.privileged_files()
        missing: list[str] = []
        for path in paths:
            state = audit.audit_rule_state(rf"{re.escape(str(path))}")
            if not state.valid:
                missing.append(f"{path}: running={state.running}, persistent={state.persistent}")
        passed = not missing
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="all privileged commands are audited" if passed else "privileged commands are missing from audit configuration",
            expected="every setuid/setgid file is present in running and persistent audit configuration",
            found="no privileged files found" if not paths else ("all files audited" if passed else "; ".join(missing)),
        )


class NetplanRule(AuditRuleSetRule):
    rule_id = "6.2.3.9"
    title = "Ensure events that modify /etc/netplan are collected"
    _PATTERNS = (watch("/etc/netplan", "system-locale"),)

    def check(self) -> ScanResult:
        if not Path("/etc/netplan").exists():
            return ScanResult(
                rule_id=self.rule_id, title=self.title, passed=True,
                message="/etc/netplan does not exist; not applicable.",
                expected="/etc/netplan is watched if it exists", found="/etc/netplan not present",
            )
        return super().check()


class ImmutableAuditRule(CISRule):
    rule_id = "6.2.3.29"
    title = "Ensure the audit configuration is immutable"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        try:
            files = sorted(audit.AUDIT_RULES_DIRECTORY.glob("*.rules"))
        except OSError:
            files = []
        lines: list[str] = []
        for path in files:
            try:
                lines.extend(path.read_text(errors="ignore").splitlines())
            except OSError:
                continue
        matches = [line for line in lines if re.match(r"^\s*-e\s+2\b", line)]
        passed = bool(matches)
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="audit configuration is immutable" if passed else "audit configuration is not immutable",
            expected="the last persistent audit rule is -e 2",
            found=matches[-1] if matches else "no persistent audit rules found",
        )
