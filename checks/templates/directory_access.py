from core import CISRule, Mode, ScanResult
from utils import permissions


class DirectoryAccess(CISRule):
    _PATH = ""
    _MAX_ACCESS = 0o0

    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:

        current_mode = permissions.mode(self._PATH)
        current_owner = permissions.owner(self._PATH)
        current_group = permissions.group(self._PATH)

        passed = (
            permissions.at_most(current_mode, self._MAX_ACCESS)
            and current_owner == 0
            and current_group == 0
        )

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "Permissions are correctly configured."
                if passed
                else "Incorrect ownership or permissions."
            ),
            expected=f"owner=root group=root mode<={self._MAX_ACCESS:03o}",
            found=f"owner={current_owner} group={current_group} mode={current_mode:03o}",
        )
