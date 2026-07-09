from core import CISRule, Mode, ScanResult
from utils import kernel_utils


class KernelModuleRule(CISRule):
    mode = Mode.AUTOMATIC

    _MODULE = ""
    rule_id = ""
    title = ""

    def check(self) -> ScanResult:
        if not kernel_utils.is_available(self._MODULE, "fs"):
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=True,
                message=f"'{self._MODULE}' module is not available on the system.",
            )

        loaded = kernel_utils.is_loaded(self._MODULE)
        config = kernel_utils.get_config(self._MODULE)
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
            expected=f"blacklist {self._MODULE}; install {self._MODULE} /bin/false (or /bin/true); module not loaded",
            found=(
                f"loaded={loaded}, blacklisted={config['blacklisted']}, "
                f"install_disabled={config['install_disabled']}"
            ),
        )
