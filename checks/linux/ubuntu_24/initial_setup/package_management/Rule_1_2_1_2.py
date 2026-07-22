import re

from core import CISRule, Mode, ScanResult
from utils.command import run


class Rule_1_2_1_2(CISRule):
    rule_id = "1.2.1.2"
    title = "Ensure weak dependencies are configured"
    server_lvl = 2
    workstation_lvl = 2
    mode = Mode.AUTOMATIC

    _RECOMMENDS = 'APT::Install-Recommends "0";'
    _SUGGESTS = 'APT::Install-Suggests "0";'

    def check(self) -> ScanResult:
        result = run("/usr/bin/apt-config dump")
        output = result.stdout if result.ok else ""

        recommends = re.search(re.escape(self._RECOMMENDS), output) is not None
        suggests = re.search(re.escape(self._SUGGESTS), output) is not None
        passed = recommends and suggests

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "APT weak dependencies are disabled"
                if passed
                else "APT weak dependencies are not fully disabled"
            ),
            expected=f"{self._RECOMMENDS} {self._SUGGESTS}",
            found=output or "no output returned from apt-config dump",
        )
