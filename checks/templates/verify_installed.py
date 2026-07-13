from core import CISRule, Mode, ScanResult
from utils import package


class VerifyInstalledRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _PACKAGES: set[str]
    _VERIFY_UPTODATE: bool = False

    def check(self) -> ScanResult:
        installed = package.installed(*self._PACKAGES)

        if installed.valid:
            message = f"package(s) ({', '.join(self._PACKAGES)}) installed"
        else:
            message = f"package(s) ({', '.join(installed.anomalies)}) missing"

        if not self._VERIFY_UPTODATE or not installed.valid:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=installed.valid,
                message=message,
            )
        else:
            uptodate = package.up_to_date(*self._PACKAGES)
            if uptodate.valid:
                message += f"; package(s) ({', '.join(self._PACKAGES)}) up to date"
            else:
                message += f"; package(s) ({', '.join(uptodate.anomalies)}) outdated"

            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=uptodate.valid,
                message=message,
            )


class VerifyNotInstalledRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _PACKAGES: set[str]

    def check(self) -> ScanResult:
        not_installed = package.not_installed(*self._PACKAGES)

        if not_installed.valid:
            message = f"package(s) ({', '.join(self._PACKAGES)}) not installed"
        else:
            message = f"package(s) ({', '.join(not_installed.anomalies)}) installed"

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=not_installed.valid,
            message=message,
        )
