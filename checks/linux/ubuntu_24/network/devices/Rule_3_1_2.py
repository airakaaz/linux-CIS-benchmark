from core import CISRule, Mode, ScanResult
from utils import kernel_utils


class Rule_3_1_2(CISRule):
    rule_id = "3.1.2"
    title = "Ensure wireless interfaces are not available"
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        modules = kernel_utils.wireless_modules()
        issues: list[str] = []
        for module in modules:
            config = kernel_utils.get_config(module)
            if not kernel_utils.is_load_disabled(module):
                issues.append(f"{module} is loadable")
            if kernel_utils.is_loaded(module):
                issues.append(f"{module} is loaded")
            if not config["blacklisted"]:
                issues.append(f"{module} is not blacklisted")

        passed = not issues
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "no wireless NIC modules are available"
                if passed and not modules
                else "wireless NIC modules are disabled"
                if passed
                else "; ".join(issues)
            ),
            expected="wireless modules are not loadable, not loaded, and blacklisted",
            found="no wireless modules" if not modules else ", ".join(issues) if issues else ", ".join(modules),
        )
