import re
from pathlib import Path
from core import CISRule, Mode, ScanResult


class Rule_1_7_7(CISRule):
    rule_id = "1.7.7"
    title = "Ensure Xwayland is configured"
    mode = Mode.AUTOMATIC

    _CONFIG = "/etc/gdm/custom.conf"

    _OPTION_RE = re.compile(r"^\s*WaylandEnable\s*=\s*(\S+)", re.IGNORECASE)

    def _daemon_section_lines(self, content: str) -> list[str]:
        lines: list[str] = []
        in_section = False
        for line in content.splitlines():
            if "[daemon]" in line.lower():
                in_section = True
                continue
            if "[" in line:
                in_section = False
                continue
            if in_section:
                lines.append(line)
        return lines

    def check(self) -> ScanResult:
        cfg = Path(self._CONFIG)

        if not cfg.is_file():
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=False,
                message=f"{self._CONFIG} not found.",
                expected=f"WaylandEnable=false in [daemon] section of {self._CONFIG}",
                found=f"{self._CONFIG} does not exist",
            )

        content = cfg.read_text(errors="ignore")

        value = None
        for line in self._daemon_section_lines(content):
            match = self._OPTION_RE.match(line)
            if match:
                value = match.group(1)

        passed = value is not None and value.lower() == "false"

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "WaylandEnable is set to false in the [daemon] section."
                if passed
                else f"WaylandEnable is not set to false (found: {value!r})."
            ),
            expected=f"WaylandEnable=false in [daemon] section of {self._CONFIG}",
            found=(
                f"WaylandEnable={value!r}"
                if value is not None
                else "WaylandEnable not set in [daemon] section"
            ),
        )
