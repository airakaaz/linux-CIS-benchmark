import re

from core import CISRule, Mode, ScanResult
from utils import audit


class Rule_6_2_3_29(CISRule):
    rule_id = "6.2.3.29"
    title = "Ensure the audit configuration is immutable"
    workstation_lvl = 2
    server_lvl = 2
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
            message="audit configuration is immutable"
            if passed
            else "audit configuration is not immutable",
            expected="the last persistent audit rule is -e 2",
            found=matches[-1] if matches else "no persistent audit rules found",
        )
