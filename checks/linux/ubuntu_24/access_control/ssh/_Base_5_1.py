from pathlib import Path

from core import CISRule, Mode, ScanResult
from checks.templates.file_content import get_os_id
from utils import filesystem, permissions, ssh


class SshAccessRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def access_result(
        self,
        paths: list[Path],
        *,
        max_mode: int,
        expected: str,
        require_paths: bool = True,
    ) -> ScanResult:
        anomalies, missing = permissions.check_paths(paths, max_mode=max_mode)
        issues = [
            *(f"{path} has incorrect mode, owner, or group" for path in anomalies),
            *(f"{path} is missing" for path in missing if require_paths),
        ]
        passed = not issues and (bool(paths) or not require_paths)
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "SSH files are correctly configured."
                if passed
                else "; ".join(issues) or "No applicable SSH files were found."
            ),
            expected=expected,
            found="compliant" if passed else "; ".join(issues) or "none",
        )


class SshBannerRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        banner = ssh.banner()
        if not banner:
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=False,
                message="sshd Banner is not configured.",
                expected="Banner points to a file without system information",
                found="Banner none or sshd configuration could not be read",
            )

        path = Path(banner)
        if not path.is_file():
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=False,
                message=f"sshd Banner file {banner} does not exist.",
                expected="Banner points to an existing file without system information",
                found=banner,
            )

        os_id = get_os_id()
        patterns = [r"\\[vrms]"]
        if os_id:
            patterns.append(rf"\b{os_id}\b")
        matched = filesystem.contains_regex([banner], rf"(?:{'|'.join(patterns)})")

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=not matched.found,
            message=(
                "sshd Banner is configured without system information."
                if not matched.found
                else "sshd Banner contains system information."
            ),
            expected="Banner file contains no system-information escape sequences or OS identifier",
            found=banner
            if not matched.found
            else f"matched in {', '.join(matched.locations)}",
        )


class SshdOptionRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC
    _OPTION = ""

    def option_value(self) -> str | None:
        values = ssh.effective_options().get(self._OPTION, [])
        return values[-1] if values else None

    def is_compliant(self, value: str | None) -> bool:
        return value is not None

    def expected_value(self) -> str:
        return self._OPTION

    def check(self) -> ScanResult:
        value = self.option_value()
        passed = self.is_compliant(value)
        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                f"sshd {self._OPTION} is configured correctly"
                if passed
                else f"sshd {self._OPTION} is not configured correctly"
            ),
            expected=self.expected_value(),
            found=value or "not set",
        )
