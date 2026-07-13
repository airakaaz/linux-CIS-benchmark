import re
from pathlib import Path
from core import CISRule, Mode, ScanResult


class Rule_1_7_6(CISRule):
    rule_id = "1.7.6"
    title = "Ensure XDMCP is not enabled"
    mode = Mode.AUTOMATIC

    _CANDIDATE_FILES = [
        "/etc/gdm3/custom.conf",
        "/etc/gdm3/daemon.conf",
        "/etc/gdm/custom.conf",
        "/etc/gdm/daemon.conf",
    ]

    _HAS_XDMCP_SECTION_RE = re.compile(r"^\s*\[xdmcp\]", re.IGNORECASE | re.MULTILINE)

    _ENABLE_TRUE_RE = re.compile(r"^\s*Enable\s*=\s*true")

    def _enabled_lines_in_xdmcp_block(self, content: str) -> list[str]:
        matches: list[str] = []
        in_section = False
        for line in content.splitlines():
            if "[xdmcp]" in line:
                in_section = True
                continue
            if "[" in line:
                in_section = False
                continue
            if in_section and self._ENABLE_TRUE_RE.match(line):
                matches.append(line.strip())
        return matches

    def check(self) -> ScanResult:
        anomalies: list[str] = []

        for path_str in self._CANDIDATE_FILES:
            path = Path(path_str)
            if not path.is_file():
                continue

            content = path.read_text(errors="ignore")
            if not self._HAS_XDMCP_SECTION_RE.search(content):
                continue

            for line in self._enabled_lines_in_xdmcp_block(content):
                anomalies.append(f'{path_str}: "{line}"')

        passed = not anomalies

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "No GDM configuration file has XDMCP enabled."
                if passed
                else "XDMCP is enabled: " + "; ".join(anomalies) + "."
            ),
            expected="no [xdmcp] block with Enable=true in any GDM config file",
            found="none found" if passed else "; ".join(anomalies),
        )
