from core import CISRule, Mode, ScanResult
from utils import package, systemctl


def evaluate(
    packages: tuple[str, ...], mode: str, services: tuple[str, ...]
) -> tuple[bool, str]:

    pkg_result = package.not_installed(*packages, mode=mode)

    if pkg_result.valid:
        return True, f"{', '.join(packages)} not installed"

    installed = pkg_result.anomalies
    no_dependents = {pkg for pkg in installed if not package.is_dependency(pkg)}

    if no_dependents:
        return False, (
            f"{', '.join(sorted(no_dependents))} installed and not required "
            f"as a dependency of any other installed package; should be removed"
        )

    enabled = any(systemctl.is_enabled(s) for s in services)
    active = any(systemctl.is_active(s) for s in services)
    passed = not enabled and not active

    installed_summary = ", ".join(sorted(installed))
    services_summary = ", ".join(services)

    if passed:
        detail = (
            f"{installed_summary} installed as a required dependency; "
            f"{services_summary} neither enabled nor active "
            f"(verify site policy approval)"
        )
    else:
        states = []
        if enabled:
            states.append("enabled")
        else:
            states.append("not enabled")
        if active:
            states.append("active")
        else:
            states.append("not active")
        detail = (
            f"{installed_summary} installed and {services_summary} is "
            f"{' and '.join(states)}"
        )

    return passed, detail


class PackageNotInstalledRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    _PACKAGES: tuple[str, ...]
    _MODE: str = "s"
    _SERVICES: tuple[str, ...]

    def check(self) -> ScanResult:
        passed, detail = evaluate(self._PACKAGES, self._MODE, self._SERVICES)

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=detail,
            expected=(
                f"{', '.join(self._PACKAGES)} not installed, OR installed "
                f"only as a required dependency with "
                f"{', '.join(self._SERVICES)} neither enabled nor active "
                f"(approved by site policy)"
            ),
            found=detail,
        )
