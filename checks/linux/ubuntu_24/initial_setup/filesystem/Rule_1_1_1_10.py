from core import ScanResult
from core import CISRule, Mode
from utils import kernel_module


class Rule_1_1_1_10(CISRule):
    rule_id = "1.1.1.10"
    title = "Ensure usb-storage kernel module is not available"
    mode = Mode.AUTOMATIC

    _MODULE = "usb-storage"

    def check(self) -> ScanResult:
        if not kernel_module.is_available(self._MODULE, "fs"):
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message=f"'{self._MODULE}' module is not available on the system.",
            )

        loaded = kernel_module.is_loaded(self._MODULE)
        config = kernel_module.get_config(self._MODULE)
        passed = (not loaded) and config["blacklisted"] and config["install_disabled"]

        if passed:
            message = (
                f"'{self._MODULE}' module is available but is not loaded, "
                "is blacklisted, and is disabled via install directive."
            )
        else:
            reasons = []
            if loaded:
                reasons.append("module is currently loaded")
            if not config["blacklisted"]:
                reasons.append("module is not blacklisted")
            if not config["install_disabled"]:
                reasons.append("module is not disabled via install directive")
            message = (
                f"'{self._MODULE}' module is not fully disabled: {', '.join(reasons)}."
            )

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
            expected="blacklist usb-storage; install usb-storage /bin/false (or /bin/true); module not loaded",
            found=(
                f"loaded={loaded}, blacklisted={config['blacklisted']}, "
                f"install_disabled={config['install_disabled']}"
            ),
        )
