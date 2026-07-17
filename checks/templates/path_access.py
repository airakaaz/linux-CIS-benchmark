from pathlib import Path

from core import CISRule, Mode, ScanResult
from utils import filesystem, permissions


class MultiPathsAccessRule(CISRule):
    _PATHS: list[str]
    _MAX_ACCESS: int
    _VALID_OWNERS: set[int] = {0}
    _VALID_GROUPS: set[int] = {0}

    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:

        passed = True
        anomalies = []
        for path in self._PATHS:
            if not Path(path).exists():
                continue

            current_mode = permissions.mode(path)
            current_owner = permissions.owner(path)
            current_group = permissions.group(path)

            if not (
                permissions.at_most(current_mode, self._MAX_ACCESS)
                and current_owner in self._VALID_OWNERS
                and current_group in self._VALID_GROUPS
            ):
                anomalies.append(path)
                passed = False

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "Permissions are correctly configured."
                if passed
                else f"Incorrect ownership or permissions for : ({', '.join(anomalies)})"
            ),
        )


class PathAccessRule(MultiPathsAccessRule):
    _PATH: str

    def __init_subclass__(cls, **kwargs) -> None:
        super.__init_subclass__(**kwargs)
        cls._PATHS = [cls._PATH]
