import re
from pathlib import Path
from core import CISRule, Mode, ScanResult


class Rule_1_4_1(CISRule):
    rule_id = "1.4.1"
    title = "Ensure bootloader password is set"
    server_lvl = 1
    workstation_lvl = 1
    mode = Mode.AUTOMATIC

    _GRUB_CFG = "/boot/grub/grub.cfg"

    _SUPERUSERS_RE = re.compile(r'^\s*set\s+superusers\s*=\s*"([^"]+)"', re.MULTILINE)
    _PASSWORD_RE = re.compile(r"^\s*password_pbkdf2\s+(\S+)\s+(\S+)", re.MULTILINE)

    def check(self) -> ScanResult:
        cfg = Path(self._GRUB_CFG)

        if not cfg.is_file():
            return ScanResult(
                rule_id=self.rule_id,
                title=self.title,
                passed=False,
                message=f"{self._GRUB_CFG} not found.",
                expected='set superusers="<user>" and password_pbkdf2 present in grub.cfg',
                found=f"{self._GRUB_CFG} does not exist",
            )

        content = cfg.read_text(errors="ignore")

        superusers_match = self._SUPERUSERS_RE.search(content)
        superusers = (
            {
                name.strip()
                for name in superusers_match.group(1).split(",")
                if name.strip()
            }
            if superusers_match
            else set()
        )

        passwords: dict[str, str] = {}
        for username, pw_hash in self._PASSWORD_RE.findall(content):
            passwords[username] = pw_hash

        missing_password_for = {
            user for user in superusers if user not in passwords or not passwords[user]
        }

        passed = bool(superusers) and not missing_password_for

        if passed:
            message = (
                f"Bootloader superuser(s) {', '.join(sorted(superusers))} "
                f"configured with password_pbkdf2."
            )
        elif not superusers:
            message = "No bootloader superuser is set."
        else:
            message = (
                f"Bootloader superuser(s) missing a password_pbkdf2 entry: "
                f"{', '.join(sorted(missing_password_for))}."
            )

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=message,
            expected='set superusers="<user>" with a matching password_pbkdf2 <user> <hash> entry',
            found=(
                f"superusers={sorted(superusers) or 'none'}; "
                f"password_pbkdf2 users={sorted(passwords) or 'none'}"
            ),
        )
