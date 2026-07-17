import re

from core import CISRule, Mode, ScanResult
from utils import filesystem


def get_os_id() -> str:
    try:
        for line in filesystem.read("/etc/os-release").splitlines():
            if line.startswith("ID="):
                return line[3:].strip().strip('"')
    except OSError:
        pass

    return ""


class NoSystemInformationRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _PATHS: list[str]
    _PATH_PATTERNS: tuple[str, ...] = ()

    def get_paths(self) -> list[str]:
        return (
            filesystem.resolve_paths(*self._PATH_PATTERNS)
            if self._PATH_PATTERNS
            else self._PATHS
        )

    def check(self) -> ScanResult:
        paths = self.get_paths()
        os_id = get_os_id()
        patterns = [r"\\[vrms]"]
        if os_id:
            patterns.append(rf"\b{re.escape(os_id)}\b")

        forbidden = rf"(?:{'|'.join(patterns)})"
        matched = filesystem.contains_regex(paths, forbidden)

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=not matched.found,
            message=(
                "files do not contain system information"
                if not matched.found
                else "files contain system information"
            ),
            expected=f"no matches for {forbidden} in ({', '.join(paths)})",
            found=(
                f"matched in ({', '.join(matched.locations)})"
                if matched.found
                else "no matching files"
            ),
        )


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
