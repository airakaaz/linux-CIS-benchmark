import re

from core import CISRule, Mode, ScanResult
from utils.command import run


class UfwDefaultPolicyRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _FIELD_INDEX: int = 0
    _ALLOWED_PREFIXES: tuple[str, ...] = ()

    def _default_line(self) -> str:
        result = run("ufw status verbose")
        if not result.ok:
            return ""

        for line in result.stdout.splitlines():
            if line.startswith("Default:"):
                return line

        return ""

    def _field_value(self, line: str) -> str:
        fields = [field.strip() for field in line.split(",")]
        if len(fields) <= self._FIELD_INDEX:
            return ""
        return fields[self._FIELD_INDEX]

    def _matches_policy(self, value: str) -> bool:
        return any(
            re.match(rf"^{re.escape(prefix)}\b", value, flags=re.IGNORECASE)
            for prefix in self._ALLOWED_PREFIXES
        )

    def check(self) -> ScanResult:
        default_line = self._default_line()
        field_value = self._field_value(default_line)
        passed = bool(field_value) and self._matches_policy(field_value)

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "ufw default policy is configured correctly"
                if passed
                else "ufw default policy is not configured correctly"
            ),
            expected=(
                f"Default policy field {self._FIELD_INDEX + 1} starts with "
                f"{', '.join(self._ALLOWED_PREFIXES)}"
            ),
            found=field_value or "no default policy line found",
        )
