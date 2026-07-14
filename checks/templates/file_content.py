import re

from core import CISRule, Mode, ScanResult
from utils import filesystem


class RequireFileContentRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _PATHS: list[str]
    _PATTERN: str

    def check(self) -> ScanResult:
        matched: list[str] = []
        missing: list[str] = []

        for file in self._PATHS:
            match = filesystem.contains_regex([file], self._PATTERN, re.MULTILINE)

            if match.found:
                matched.extend(match.locations)
            else:
                missing.append(file)

        passed = not missing

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "required content found"
                if passed
                else f"required content missing in ({', '.join(missing)})"
            ),
            expected=f"pattern {self._PATTERN} in ({', '.join(self._PATHS)})",
            found=(
                f"matched in ({', '.join(matched)})"
                if matched
                else "no matching files"
            ),
        )
