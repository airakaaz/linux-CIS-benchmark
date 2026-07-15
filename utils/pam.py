from pathlib import Path
import re


FAILLOCK_CONF = Path("/etc/security/faillock.conf")
PWQUALITY_CONF = Path("/etc/security/pwquality.conf")
PWQUALITY_CONF_DIRECTORY = Path("/etc/security/pwquality.conf.d")
PWHISTORY_CONF = Path("/etc/security/pwhistory.conf")
COMMON_AUTH = Path("/etc/pam.d/common-auth")
COMMON_PASSWORD = Path("/etc/pam.d/common-password")
PAM_UNIX_FILES = tuple(
    Path(f"/etc/pam.d/common-{name}")
    for name in ("password", "auth", "account", "session", "session-noninteractive")
)


def active_lines(path: Path) -> list[str]:
    try:
        return [
            line.split("#", 1)[0].strip()
            for line in path.read_text(errors="ignore").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
    except OSError:
        return []


def option_values(path: Path, option: str) -> list[str]:
    pattern = re.compile(rf"^\s*{re.escape(option)}\s*=\s*([^\s#]+)", re.IGNORECASE)
    return [
        match.group(1)
        for line in active_lines(path)
        if (match := pattern.match(line))
    ]


def config_values(path: Path, option: str) -> list[str]:
    return option_values(path, option)


def pwquality_files() -> list[Path]:
    files = []
    if PWQUALITY_CONF.is_file():
        files.append(PWQUALITY_CONF)
    try:
        files.extend(sorted(PWQUALITY_CONF_DIRECTORY.glob("*.conf")))
    except OSError:
        pass
    return files


def pwquality_values(option: str) -> list[str]:
    values: list[str] = []
    for path in pwquality_files():
        values.extend(option_values(path, option))
    return values


def module_lines(module: str, path: Path) -> list[str]:
    pattern = re.compile(rf"^\s*\S+\s+[^#\n\r]*\b{re.escape(module)}\.so\b", re.IGNORECASE)
    return [line for line in active_lines(path) if pattern.search(line)]


def module_arguments(module: str, option: str, path: Path) -> list[str | None]:
    pattern = re.compile(
        rf"(?:^|\s){re.escape(option)}(?:\s*=\s*([^\s]+))?(?=\s|$)",
        re.IGNORECASE,
    )
    values: list[str | None] = []
    for line in module_lines(module, path):
        values.extend(match.group(1) for match in pattern.finditer(line))
    return values


def _numeric(values: list[str], minimum: int, maximum: int | None = None) -> bool:
    if not values:
        return False
    try:
        numbers = [int(value) for value in values]
    except ValueError:
        return False
    return all(number >= minimum and (maximum is None or number <= maximum) for number in numbers)


def faillock_deny() -> tuple[bool, str]:
    values = config_values(FAILLOCK_CONF, "deny")
    pam_values = [value for value in module_arguments("pam_faillock", "deny", COMMON_AUTH) if value is not None]
    passed = _numeric(values, 1, 5) and (
        not pam_values or _numeric(pam_values, 1, 5)
    )
    return passed, f"faillock deny={values or 'not set'}; PAM deny={pam_values or 'not set'}"


def faillock_unlock_time() -> tuple[bool, str]:
    values = config_values(FAILLOCK_CONF, "unlock_time")
    pam_values = [value for value in module_arguments("pam_faillock", "unlock_time", COMMON_AUTH) if value is not None]

    def valid(items: list[str]) -> bool:
        if not items:
            return False
        try:
            return all(int(item) == 0 or int(item) >= 900 for item in items)
        except ValueError:
            return False

    try:
        pam_valid = all(int(value) == 0 or int(value) >= 900 for value in pam_values)
    except ValueError:
        pam_valid = False
    passed = valid(values) and (not pam_values or pam_valid)
    return passed, f"faillock unlock_time={values or 'not set'}; PAM unlock_time={pam_values or 'not set'}"


def faillock_root() -> tuple[bool, str]:
    lines = active_lines(FAILLOCK_CONF)
    even_deny_root = any(re.match(r"^\s*even_deny_root\s*$", line, re.IGNORECASE) for line in lines)
    values = config_values(FAILLOCK_CONF, "root_unlock_time")
    pam_values = [value for value in module_arguments("pam_faillock", "root_unlock_time", COMMON_AUTH) if value is not None]
    try:
        valid_values = all(int(value) >= 60 for value in values + pam_values)
    except ValueError:
        valid_values = False
    passed = (even_deny_root or bool(values)) and valid_values
    return passed, f"even_deny_root={even_deny_root}; root_unlock_time={values or pam_values or 'not set'}"


def pwquality_numeric(option: str, minimum: int, maximum: int | None = None) -> tuple[bool, str]:
    values = pwquality_values(option)
    pam_values = [value for value in module_arguments("pam_pwquality", option, COMMON_PASSWORD) if value is not None]
    passed = _numeric(values, minimum, maximum) and all(
        _numeric([value], minimum, maximum) for value in pam_values
    )
    return passed, f"{option}={values or 'not set'}; PAM {option}={pam_values or 'not set'}"


def pwquality_not_zero(option: str) -> tuple[bool, str]:
    values = pwquality_values(option)
    pam_values = [value for value in module_arguments("pam_pwquality", option, COMMON_PASSWORD) if value is not None]
    try:
        passed = all(int(value) != 0 for value in values + pam_values)
    except ValueError:
        passed = False
    return passed, f"{option}={values or 'not set'}; PAM {option}={pam_values or 'not set'}"


def pwquality_flag(option: str) -> tuple[bool, str]:
    values = [line for path in pwquality_files() for line in active_lines(path) if re.match(rf"^\s*{re.escape(option)}\s*$", line, re.IGNORECASE)]
    return bool(values), f"{option}: {'configured' if values else 'not configured'}"


def pwhistory_option(option: str, minimum: int | None = None) -> tuple[bool, str]:
    if PWHISTORY_CONF.is_file():
        values = option_values(PWHISTORY_CONF, option)
        if minimum is None:
            passed = bool(values)
        else:
            passed = _numeric(values, minimum)
        return passed, f"pwhistory.conf {option}={values or 'not set'}"

    values = [value for value in module_arguments("pam_pwhistory", option, COMMON_PASSWORD) if value is not None]
    if minimum is None:
        passed = bool(module_arguments("pam_pwhistory", option, COMMON_PASSWORD))
    else:
        passed = _numeric(values, minimum)
    return passed, f"PAM {option}={values or 'not set'}"


def pam_unix_absent(option: str) -> tuple[bool, str]:
    matches = [
        line
        for path in PAM_UNIX_FILES
        for line in module_lines("pam_unix", path)
        if re.search(rf"(?:^|\s){re.escape(option)}(?:=\d+)?(?=\s|$)", line)
    ]
    return not matches, "; ".join(matches) or "not present"


def pam_unix_argument(option: str) -> tuple[bool, str]:
    lines = module_lines("pam_unix", COMMON_PASSWORD)
    matches = [line for line in lines if re.search(rf"(?:^|\s){re.escape(option)}(?=\s|$)", line)]
    return bool(matches), "; ".join(matches) or "not present"


def pam_unix_hash() -> tuple[bool, str]:
    lines = module_lines("pam_unix", COMMON_PASSWORD)
    matches = [line for line in lines if re.search(r"(?:^|\s)(?:sha512|yescrypt)(?=\s|$)", line, re.IGNORECASE)]
    return bool(matches), "; ".join(matches) or "no sha512/yescrypt hash configured"
