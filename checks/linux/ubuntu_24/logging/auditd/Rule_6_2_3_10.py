import re

from core import CISRule, Mode, ScanResult
from ._Base_6_2_3 import audit


class Rule_6_2_3_10(CISRule):
    rule_id = "6.2.3.10"
    title = "Ensure use of privileged commands are collected"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        paths = audit.privileged_files()
        missing: list[str] = []
        for path in paths:
            state = audit.audit_rule_state(rf"{re.escape(str(path))}")
            if not state.valid:
                missing.append(
                    f"{path}: running={state.running}, persistent={state.persistent}"
                )
        passed = not missing
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="all privileged commands are audited"
            if passed
            else "privileged commands are missing from audit configuration",
            expected="every setuid/setgid file is present in running and persistent audit configuration",
            found="no privileged files found"
            if not paths
            else ("all files audited" if passed else "; ".join(missing)),
        )
