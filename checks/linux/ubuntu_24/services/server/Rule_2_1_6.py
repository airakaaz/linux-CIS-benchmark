from core import CISRule, Mode, ScanResult
from ._Base_2_1 import evaluate


class Rule_2_1_6(CISRule):
    rule_id = "2.1.6"
    title = "Ensure web server services are not in use"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.AUTOMATIC

    _COMPONENTS = (
        ("apache2", ("apache2",), "s", ("apache2.socket", "apache2.service")),
        ("nginx", ("nginx",), "s", ("nginx.service",)),
    )

    def check(self) -> ScanResult:
        details = []
        passed = True

        for name, packages, mode_, services in self._COMPONENTS:
            component_passed, detail = evaluate(packages, mode_, services)
            details.append(f"{name}: {detail}")
            if not component_passed:
                passed = False

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="; ".join(details),
            expected=(
                "apache2 and nginx not installed, OR installed only as a "
                "required dependency with their service(s)/socket(s) "
                "neither enabled nor active (approved by site policy). "
                "Other web server packages should be audited the same way."
            ),
            found="; ".join(details),
        )
