import re
from pathlib import Path

from core import CISRule, Mode, ScanResult
from utils import permissions


class Rule_1_2_1_3(CISRule):
    rule_id = "1.2.1.3"
    title = "Ensure apt key files and signed-by sources are configured securely"
    mode = Mode.AUTOMATIC

    _KEY_DIRECTORIES = [
        "/usr/share/keyrings",
        "/etc/apt/trusted.gpg.d",
    ]
    _SOURCES_DIRECTORY = Path("/etc/apt/sources.list.d")
    _SIGNED_BY_RE = re.compile(r"^([^#\n\r]+)?\bSigned-By\b", re.IGNORECASE | re.MULTILINE)

    def _bad_key_files(self) -> list[str]:
        bad_files: list[str] = []

        for directory in self._KEY_DIRECTORIES:
            path = Path(directory)
            if not path.exists():
                continue

            for file in path.rglob("*gpg"):
                if not file.is_file():
                    continue

                if (
                    permissions.owner(str(file)) != 0
                    or permissions.group(str(file)) != 0
                    or not permissions.at_most(permissions.mode(str(file)), 0o644)
                ):
                    bad_files.append(str(file))

        return bad_files

    def _bad_signed_by_files(self) -> list[str]:
        bad_files: list[str] = []

        if not self._SOURCES_DIRECTORY.exists():
            return bad_files

        for file in self._SOURCES_DIRECTORY.rglob("*.list"):
            if file.is_file() and self._SIGNED_BY_RE.search(file.read_text(errors="ignore")):
                if (
                    permissions.owner(str(file)) != 0
                    or permissions.group(str(file)) != 0
                    or not permissions.at_most(permissions.mode(str(file)), 0o644)
                ):
                    bad_files.append(str(file))

        for file in self._SOURCES_DIRECTORY.rglob("*.sources"):
            if file.is_file() and self._SIGNED_BY_RE.search(file.read_text(errors="ignore")):
                if (
                    permissions.owner(str(file)) != 0
                    or permissions.group(str(file)) != 0
                    or not permissions.at_most(permissions.mode(str(file)), 0o644)
                ):
                    bad_files.append(str(file))

        return bad_files

    def check(self) -> ScanResult:
        bad_files = self._bad_key_files() + self._bad_signed_by_files()
        passed = not bad_files

        return ScanResult(
            rule_id=self.rule_id,
            title=self.title,
            passed=passed,
            message=(
                "apt key and signed-by source files are configured securely"
                if passed
                else "insecure apt files found"
            ),
            expected="root:root ownership with mode 0644 or more restrictive",
            found="; ".join(bad_files) if bad_files else "none",
        )
