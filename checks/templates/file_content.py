import re
from pathlib import Path

from core import CISRule, Mode, ScanResult
from utils import filesystem


class VerifyFileContentRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _PATHS: list[str]
    _PATTERN: str

    def check(self) -> ScanResult:
        match = filesystem.contains_regex(self._PATHS, self._PATTERN, re.MULTILINE)

        passed = not match.found

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "no forbidden content found"
                if passed
                else f"forbidden content found in ({', '.join(match.locations)})"
            ),
        )
