from core import CISRule, Mode, ScanResult
from utils import permissions, rsyslog

from checks.templates.verify_installed import VerifyInstalledRule
from checks.templates.service_status import EnabledServiceRule


class RsyslogFileCreateModeRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        values = rsyslog.file_create_modes()
        passed = bool(values) and all(permissions.at_most(value, 0o640) for value in values)
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="$FileCreateMode is configured correctly" if passed else "$FileCreateMode is missing or too permissive",
            expected="$FileCreateMode 0640 or more restrictive", found=", ".join(f"{value:04o}" for value in values) or "not set",
        )


class RsyslogRemoteInputRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        matches = rsyslog.receives_remote_logs()
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=not matches,
            message="rsyslog does not accept remote logs" if not matches else "rsyslog accepts remote logs",
            expected="no imtcp or InputTCPServerRun configuration", found="none" if not matches else "; ".join(matches),
        )


class RsyslogGtlsRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        matches = rsyslog.gtls_forwarding()
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=bool(matches),
            message="rsyslog forwarding uses gtls" if matches else "rsyslog gtls forwarding is not configured",
            expected='StreamDriver="gtls"', found="; ".join(matches) if matches else "not set",
        )
