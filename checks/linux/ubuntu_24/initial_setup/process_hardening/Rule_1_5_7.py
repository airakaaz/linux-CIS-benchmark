import re
from pathlib import Path

from core import CISRule, Mode, ScanResult
from utils import systemctl, package


class Rule_1_5_7(CISRule):
    rule_id = "1.5.7"
    title = "Ensure Automatic Error Reporting is configured"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.AUTOMATIC

    _PACKAGE = "apport"
    _SERVICE = "apport.service"
    _CONFIG = "/etc/default/apport"

    _ENABLED_RE = re.compile(r"^\s*enabled\s*=\s*[^0]\b", re.IGNORECASE | re.MULTILINE)

    def check(self) -> ScanResult:
        installed = package.installed(self._PACKAGE).valid

        config_enabled = False
        if installed:
            cfg = Path(self._CONFIG)
            if cfg.is_file():
                content = cfg.read_text(errors="ignore")
                config_enabled = bool(self._ENABLED_RE.search(content))

        active = systemctl.is_active(self._SERVICE)

        passed = not config_enabled and not active

        reasons = []
        if config_enabled:
            reasons.append(f"{self._CONFIG} sets enabled to a non-zero value")
        if active:
            reasons.append(f"{self._SERVICE} is active")

        message = (
            "Apport is not enabled via configuration and its service is not active."
            if passed
            else "Apport is enabled: " + "; ".join(reasons) + "."
        )

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
            expected=(
                f"if {self._PACKAGE} is installed, {self._CONFIG} 'enabled' "
                f"is not set to a non-zero value; {self._SERVICE} not active"
            ),
            found=(
                f"installed={installed}, config_enabled={config_enabled}, "
                f"service_active={active}"
            ),
        )
