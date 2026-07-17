from pathlib import Path

from core import CISRule, Mode, ScanResult
from utils import filesystem, permissions


class MultiPathsAccessRule(CISRule):
    _PATHS: list[str] | tuple[str, ...]
    _MAX_ACCESS: int
    _VALID_OWNERS: set[int] = {0}
    _VALID_GROUPS: set[int] = {0}
    _MISSING_FAIL: bool = False

    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:

        paths = filesystem.resolve_paths(*self._PATHS)

        anomalies, missing = permissions.check_paths(
            [Path(p) for p in paths],
            max_mode=self._MAX_ACCESS,
            valid_owners=self._VALID_OWNERS,
            valid_groups=self._VALID_GROUPS,
        )

        passed = not anomalies
        if self._MISSING_FAIL:
            passed = passed and not missing

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "Permissions are correctly configured."
                if passed
                else f"Incorrect ownership or permissions for : ({', '.join(map(str, anomalies))})"
            ),
        )


class PathAccessRule(MultiPathsAccessRule):
    _PATH: str

    def __init_subclass__(cls, **kwargs) -> None:
        super.__init_subclass__(**kwargs)
        cls._PATHS = [cls._PATH]
