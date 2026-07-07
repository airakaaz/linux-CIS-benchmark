from core import CISRule, Mode, ScanResult
from utils.command import run


def get_mount_options(mount_point: str) -> set[str] | None:
    result = run(f"findmnt -kn {mount_point}")
    if not result.ok or not result.stdout.strip():
        return None

    # findmnt -kn output: TARGET SOURCE FSTYPE OPTIONS
    parts = result.stdout.split()
    if len(parts) < 4:
        return None

    return set(parts[-1].split(","))


class MountOptionRule(CISRule):
    mode = Mode.AUTOMATIC
    _MOUNT_POINT: str = ""
    _OPTION: str = ""

    def check(self) -> ScanResult:
        options = get_mount_options(self._MOUNT_POINT)

        if options is None:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=False,
                message=f"'{self._MOUNT_POINT}' is not a separate mount point",
            )

        passed = self._OPTION in options
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                f"'{self._OPTION}' is "
                f"{'set' if passed else 'NOT set'} on '{self._MOUNT_POINT}'."
            ),
            expected=f"'{self._OPTION}' present in mount options for {self._MOUNT_POINT}",
            found=", ".join(sorted(options)) or "(no options)",
        )


class SeparatePartitionRule(CISRule):
    mode = Mode.AUTOMATIC

    _MOUNT_POINT: str = ""

    def check(self) -> ScanResult:
        options = get_mount_options(self._MOUNT_POINT)
        mounted = options is not None

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=mounted,
            message=(
                f"'{self._MOUNT_POINT}' is mounted as a separate partition."
                if mounted
                else f"'{self._MOUNT_POINT}' is not a separate partition."
            ),
            expected=f"'{self._MOUNT_POINT}' mounted as its own partition or filesystem",
            found="mounted separately" if mounted else "part of root filesystem",
        )
