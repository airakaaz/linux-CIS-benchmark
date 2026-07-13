from dataclasses import dataclass
from typing import Callable
import re

from core import CISRule, Mode, ScanResult
from utils import gsettings, package


@dataclass(slots=True)
class GsettingsCheck:
    schema: str
    key: str
    require_locked: bool = True
    validate: Callable[[str], bool] = lambda value: bool(value.strip())
    expected: str = "set"


_NUMERIC_PREFIX_RE = re.compile(r"^(?:u?int(?:16|32|64)|byte|double)\s+(.+)$")


def _parse_numeric(value: str) -> int | float | None:
    match = _NUMERIC_PREFIX_RE.match(value.strip())
    raw = match.group(1) if match else value.strip()
    try:
        return float(raw) if "." in raw else int(raw)
    except ValueError:
        return None


def equals(expected: str, *, case_insensitive: bool = True) -> Callable[[str], bool]:
    target = expected.lower() if case_insensitive else expected

    def _validate(value: str) -> bool:
        v = value.lower() if case_insensitive else value
        return v == target

    return _validate


def numeric_at_most(
    maximum: int, *, exclude_zero: bool = False
) -> Callable[[str], bool]:
    def _validate(value: str) -> bool:
        parsed = _parse_numeric(value)
        if parsed is None:
            return False
        if exclude_zero and parsed == 0:
            return False
        return parsed <= maximum

    return _validate


def non_empty() -> Callable[[str], bool]:
    def _validate(value: str) -> bool:
        return bool(value.strip())

    return _validate


class GsettingsRule(CISRule):
    """
    Generic template for CIS audits shaped as:
      1. verify one or more gsettings keys are locked (writable == false)
      2. verify those keys hold a compliant value

    Subclasses declare `_CHECKS`, a list of GsettingsCheck. Optionally set
    `_REQUIRED_PACKAGE` if the schema only exists when a given package is
    installed (e.g. "gdm3" for org.gnome.login-screen) -- if that package
    isn't installed, the rule passes as not-applicable instead of failing
    on missing schemas.
    """

    _CHECKS: list[GsettingsCheck] = []
    _REQUIRED_PACKAGE: str | None = None
    rule_id = ""
    title = ""
    mode = Mode.AUTOMATIC

    def check(self) -> ScanResult:
        if self._REQUIRED_PACKAGE is not None:
            if package.not_installed(self._REQUIRED_PACKAGE).valid:
                return ScanResult(
                    rule_id=self.rule_id,
                    title=self.title,
                    passed=True,
                    message=f"{self._REQUIRED_PACKAGE} is not installed; not applicable.",
                    expected="N/A",
                    found=f"{self._REQUIRED_PACKAGE} not installed",
                )

        issues: list[str] = []
        details: list[str] = []

        for c in self._CHECKS:
            writable = gsettings.writable(c.schema, c.key)
            value = gsettings.get(c.schema, c.key)

            details.append(f"{c.key}: writable={writable}, value={value!r}")

            if writable is None or value is None:
                issues.append(
                    f"{c.key}: gsettings query failed (schema/key may not exist)"
                )
                continue

            if c.require_locked and writable is not False:
                issues.append(f"{c.key} is not locked (writable by users)")

            if not c.validate(value):
                issues.append(
                    f"{c.key} = {value!r} does not meet policy (expected: {c.expected})"
                )

        passed = not issues

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "All settings are locked and correctly configured."
                if passed
                else "Issues found: " + "; ".join(issues) + "."
            ),
            expected="; ".join(f"{c.key}: {c.expected}" for c in self._CHECKS),
            found="; ".join(details),
        )
