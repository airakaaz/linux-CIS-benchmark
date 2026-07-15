from pathlib import Path

from core import CISRule, Mode, ScanResult
from utils import aide


class Rule_6_3_3(CISRule):
    rule_id = "6.3.3"
    title = "Ensure cryptographic mechanisms are used to protect the integrity of audit tools"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        if aide.executable() is None:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=False,
                message="aide is not installed",
                expected="aide is installed and profiles all audit tools with required options",
                found="aide not found",
            )

        failures: list[str] = []
        checked: list[str] = []
        for tool in aide.AIDE_AUDIT_TOOLS:
            path = Path("/sbin") / tool
            if not path.is_file():
                continue
            checked.append(str(path))
            result = aide.profile(path)
            output = result.stdout + "\n" + result.stderr
            if not result.ok or not aide.has_options(output):
                failures.append(str(path))

        passed = not failures
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "AIDE profiles all existing audit tools with the required options"
                if passed
                else "AIDE audit-tool profiles are missing or do not contain the required options"
            ),
            expected="p, i, n, u, g, s, b, acl, xattrs, and sha512 for every existing audit tool",
            found="all checked tools compliant" if passed else ", ".join(failures),
        )
