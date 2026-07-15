from core import CISRule, Mode, ScanResult
import re
from pathlib import Path
from utils import accounts
from utils.command import run


def pass_max_days():
    try:
        maximum = int(accounts.login_value("PASS_MAX_DAYS") or "-1")
    except ValueError:
        maximum = -1
    invalid = [entry[0] for entry in accounts.password_entries() if len(entry) <= 4 or not entry[4].isdigit() or not 1 <= int(entry[4]) <= 365]
    return maximum >= 1 and maximum <= 365 and not invalid, f"PASS_MAX_DAYS={maximum}; invalid users={invalid}"


def pass_warn_age():
    try:
        minimum = int(accounts.login_value("PASS_WARN_AGE") or "-1")
    except ValueError:
        minimum = -1
    invalid = [entry[0] for entry in accounts.password_entries() if len(entry) <= 6 or not entry[5].isdigit() or int(entry[5]) < 7]
    return minimum >= 7 and not invalid, f"PASS_WARN_AGE={minimum}; invalid users={invalid}"


def encrypt_method():
    value = (accounts.login_value("ENCRYPT_METHOD") or "").upper()
    return value in {"SHA512", "YESCRYPT"}, value or "not set"


def inactive_days():
    result = run("useradd -D")
    match = re.search(r"^INACTIVE=(-?\d+)", result.stdout, re.MULTILINE)
    configured = int(match.group(1)) if match else -1
    invalid = [entry[0] for entry in accounts.password_entries() if len(entry) <= 7 or not entry[6].isdigit() or not 0 <= int(entry[6]) <= 45]
    return 0 <= configured <= 45 and not invalid, f"INACTIVE={configured}; invalid users={invalid}"


def only_root_uid():
    users = [entry[0] for entry in accounts.passwd_entries() if len(entry) > 2 and entry[2] == "0"]
    return users == ["root"], ", ".join(users) or "none"


def only_root_gid_user():
    users = [entry[0] for entry in accounts.passwd_entries() if len(entry) > 3 and entry[0] not in {"sync", "shutdown", "halt", "operator"} and entry[3] == "0"]
    return users == ["root"], ", ".join(users) or "none"


def only_root_gid_group():
    try:
        groups = [line.split(":", 1)[0] for line in Path("/etc/group").read_text(errors="ignore").splitlines() if len(line.split(":")) > 2 and line.split(":")[2] == "0"]
    except OSError:
        groups = []
    return groups == ["root"], ", ".join(groups) or "none"


def root_password():
    status = accounts.root_password_status()
    return status in {"P", "L"}, status or "unknown"


def root_path():
    issues = accounts.root_path_issues()
    return not issues, "; ".join(issues) or "compliant"


def root_umask():
    issues = accounts.root_umask_issues()
    return not issues, "; ".join(issues) or "compliant"


def system_shells():
    users = accounts.system_accounts_with_valid_shell()
    return not users, ", ".join(users) or "none"


def locked_invalid_shells():
    users = accounts.nonroot_invalid_shells_unlocked()
    return not users, ", ".join(users) or "none"


def no_nologin_shell():
    try:
        lines = [line for line in Path("/etc/shells").read_text(errors="ignore").splitlines() if not line.lstrip().startswith("#")]
    except OSError:
        lines = []
    matches = [line for line in lines if re.search(r"/nologin\b", line)]
    return not matches, ", ".join(matches) or "none"


def tmout():
    issues = accounts.tmout_issues()
    return not issues, "; ".join(issues) or "compliant"


def umask():
    issues = accounts.umask_issues()
    return not issues, "; ".join(issues) or "compliant"


def future_changes():
    users = accounts.future_password_changes()
    return not users, ", ".join(users) or "none"


class AccountPolicyRule(CISRule):
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC
    _CHECK = staticmethod(lambda: (False, "not implemented"))
    _EXPECTED = ""

    def check(self) -> ScanResult:
        passed, found = self._CHECK()
        return ScanResult(
            rule_id=self.rule_id, title=self.title, passed=passed,
            message="account policy is configured correctly" if passed else found,
            expected=self._EXPECTED, found="compliant" if passed else found,
        )
