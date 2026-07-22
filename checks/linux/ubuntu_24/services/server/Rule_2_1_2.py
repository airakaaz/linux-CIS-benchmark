import re
import shutil
from pathlib import Path
from core import CISRule, Mode, ScanResult
from utils.command import run


class Rule_2_1_2(CISRule):
    rule_id = "2.1.2"
    title = "Ensure mail transfer agents are configured for local-only mode"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.AUTOMATIC

    _PORTS = ("25", "465", "587")

    def _port_is_loopback_only(self, port: str) -> bool:
        result = run("ss -plntu")
        if not result.ok:
            return True

        port_re = re.compile(rf":{port}\b")
        port_lines = [
            line for line in result.stdout.splitlines() if port_re.search(line)
        ]
        if not port_lines:
            return True

        loopback_re = re.compile(rf"\s+(127\.0\.0\.1|\[?::1\]?):{port}\b")
        return all(loopback_re.search(line) for line in port_lines)

    def _mta_interfaces(self) -> str | None:
        if shutil.which("postconf"):
            result = run("postconf -n inet_interfaces")
            return result.stdout.strip() if result.ok else ""

        if shutil.which("exim"):
            result = run("exim -bP local_interfaces")
            return result.stdout.strip() if result.ok else ""

        if shutil.which("sendmail"):
            cfg = Path("/etc/mail/sendmail.cf")
            if not cfg.is_file():
                return ""
            addrs = []
            for line in cfg.read_text(errors="ignore").splitlines():
                if re.search(r"O\s+DaemonPortOptions=", line, re.IGNORECASE):
                    match = re.search(r"Addr=([^,+]+)", line)
                    if match and match.group(1) != "127.0.0.1":
                        addrs.append(match.group(1))
            return "\n".join(addrs)

        return None

    def _evaluate_mta(self) -> tuple[bool, str]:
        interfaces = self._mta_interfaces()

        if not interfaces:
            return True, "MTA not detected or in use"

        if re.search(r"\ball\b", interfaces, re.IGNORECASE):
            return False, "MTA is bound to all network interfaces"

        if not re.search(
            r"(inet_interfaces\s*=\s*)?(0\.0\.0\.0|::1|loopback-only)",
            interfaces,
            re.IGNORECASE,
        ):
            return False, f'MTA is bound to a network interface "{interfaces}"'

        return (
            True,
            f'MTA is not bound to a non-loopback network interface "{interfaces}"',
        )

    def check(self) -> ScanResult:
        details: list[str] = []
        failures: list[str] = []

        for port in self._PORTS:
            ok = self._port_is_loopback_only(port)
            detail = (
                f'Port "{port}" is not listening on a non-loopback interface'
                if ok
                else f'Port "{port}" is listening on a non-loopback interface'
            )
            details.append(detail)
            if not ok:
                failures.append(detail)

        mta_ok, mta_detail = self._evaluate_mta()
        details.append(mta_detail)
        if not mta_ok:
            failures.append(mta_detail)

        passed = not failures

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message="; ".join(details),
            expected=(
                "Ports 25/465/587 not listening on non-loopback interfaces, "
                "and MTA (if present) bound only to loopback"
            ),
            found="; ".join(failures) if failures else "; ".join(details),
        )
