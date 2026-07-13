import grp
import pwd
from pathlib import Path
from core import CISRule, Mode, ScanResult
from utils import package, permissions

from checks.templates.path_access import PathAccessRule


class AllowDenyFileRule(CISRule):
    _PACKAGE: str = ""
    _ALLOW_FILE: str = ""
    _DENY_FILE: str = ""
    _MAX_ACCESS: int = 0o640
    _VALID_OWNER_NAMES: set[str] = {"root"}
    _VALID_GROUP_NAMES: set[str] = {"root"}
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    @staticmethod
    def _resolve_uids(names: set[str]) -> set[int]:
        uids = set()
        for name in names:
            try:
                uids.add(pwd.getpwnam(name).pw_uid)
            except KeyError:
                continue
        return uids

    @staticmethod
    def _resolve_gids(names: set[str]) -> set[int]:
        gids = set()
        for name in names:
            try:
                gids.add(grp.getgrnam(name).gr_gid)
            except KeyError:
                continue
        return gids

    def _check_file(
        self,
        path_str: str,
        *,
        required: bool,
        valid_uids: set[int],
        valid_gids: set[int],
    ) -> str | None:
        """Return an anomaly description, or None if compliant."""
        path = Path(path_str)
        if not path.exists():
            return f"{path_str} does not exist" if required else None

        current_mode = permissions.mode(path_str)
        current_owner = permissions.owner(path_str)
        current_group = permissions.group(path_str)

        compliant = (
            permissions.at_most(current_mode, self._MAX_ACCESS)
            and current_owner in valid_uids
            and current_group in valid_gids
        )
        if compliant:
            return None

        return (
            f"{path_str}: mode={oct(current_mode)}, owner uid={current_owner}, "
            f"group gid={current_group} does not meet policy"
        )

    def check(self) -> ScanResult:
        if package.not_installed(self._PACKAGE).valid:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message=f"{self._PACKAGE} is not installed; not applicable.",
                expected="N/A",
                found=f"{self._PACKAGE} not installed",
            )

        valid_uids = self._resolve_uids(self._VALID_OWNER_NAMES)
        valid_gids = self._resolve_gids(self._VALID_GROUP_NAMES)

        anomalies: list[str] = []

        allow_issue = self._check_file(
            self._ALLOW_FILE,
            required=True,
            valid_uids=valid_uids,
            valid_gids=valid_gids,
        )
        if allow_issue:
            anomalies.append(allow_issue)

        deny_issue = self._check_file(
            self._DENY_FILE,
            required=False,
            valid_uids=valid_uids,
            valid_gids=valid_gids,
        )
        if deny_issue:
            anomalies.append(deny_issue)

        passed = not anomalies

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "Allow/deny files are correctly configured."
                if passed
                else "Issues found: " + "; ".join(anomalies) + "."
            ),
            expected=(
                f"{self._ALLOW_FILE} exists, mode<={oct(self._MAX_ACCESS)}, "
                f"owner in {sorted(self._VALID_OWNER_NAMES)}, "
                f"group in {sorted(self._VALID_GROUP_NAMES)}; "
                f"{self._DENY_FILE} absent or meeting the same policy"
            ),
            found="compliant" if passed else "; ".join(anomalies),
        )
