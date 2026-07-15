from core import CISRule, Mode, ScanResult
from utils import package, systemctl


def evaluate(
    packages: tuple[str, ...], mode: str, services: tuple[str, ...]
) -> tuple[bool, str]:
    result = package.not_installed(*packages, mode=mode)
    if result.valid:
        return True, f"{', '.join(packages)} not installed"

    installed = result.anomalies
    no_dependents = {item for item in installed if not package.is_dependency(item)}
    if no_dependents:
        return False, (
            f"{', '.join(sorted(no_dependents))} installed and not required "
            "as a dependency of any other installed package; should be removed"
        )

    enabled = any(systemctl.is_enabled(service) for service in services)
    active = any(systemctl.is_active(service) for service in services)
    detail = (
        f"{', '.join(sorted(installed))} installed as a required dependency; "
        f"{', '.join(services)} neither enabled nor active (verify site policy approval)"
        if not enabled and not active
        else f"{', '.join(sorted(installed))} installed and {', '.join(services)} is "
        f"{'enabled' if enabled else 'not enabled'} and {'active' if active else 'not active'}"
    )
    return not enabled and not active, detail


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

    _PACKAGES: set[str] | tuple[str, ...]
    _ALLOW_AS_DEPENDENCY: bool = False
    _MODE: str = "s"
    _SERVICES: tuple[str, ...] = ()

    def check(self) -> ScanResult:
        if self._ALLOW_AS_DEPENDENCY:
            passed, detail = evaluate(tuple(self._PACKAGES), self._MODE, self._SERVICES)
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=passed,
                message=detail,
                expected=(
                    f"{', '.join(self._PACKAGES)} not installed, OR installed only as a "
                    f"required dependency with {', '.join(self._SERVICES)} neither enabled nor active "
                    "(approved by site policy)"
                ),
                found=detail,
            )

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
