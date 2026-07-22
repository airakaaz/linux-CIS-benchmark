from pathlib import Path
import grp
import re

from core import CISRule, Mode, ScanResult
from utils import filesystem


class Rule_5_2_7(CISRule):
    rule_id = "5.2.7"
    title = "Ensure access to the su command is restricted"
    workstation_lvl = 1
    server_lvl = 1
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        path = Path("/etc/pam.d/su")
        if not path.is_file():
            return ScanResult(self.rule_id, self.title, False, "/etc/pam.d/su is missing")
        try:
            content = filesystem.read(str(path))
        except OSError:
            return ScanResult(self.rule_id, self.title, False, "cannot read /etc/pam.d/su")

        pattern = re.compile(r"^\s*auth\s+(?:required|requisite)\s+pam_wheel\.so\s+([^#]+)", re.MULTILINE)
        groups: list[str] = []
        valid_line = False
        for match in pattern.finditer(content):
            options = match.group(1).split()
            group = next((option.split("=", 1)[1] for option in options if option.startswith("group=")), None)
            if "use_uid" in options and group:
                valid_line = True
                groups.append(group)

        missing_or_populated: list[str] = []
        for group in groups:
            try:
                if grp.getgrnam(group).gr_mem:
                    missing_or_populated.append(f"{group} contains users")
            except KeyError:
                missing_or_populated.append(f"{group} does not exist")

        passed = valid_line and not missing_or_populated
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="su access is restricted to an empty group" if passed else "su access restriction is missing or invalid",
            expected="pam_wheel required/requisite with use_uid and an empty group",
            found=", ".join(groups + missing_or_populated) if groups else "no valid pam_wheel rule",
        )
