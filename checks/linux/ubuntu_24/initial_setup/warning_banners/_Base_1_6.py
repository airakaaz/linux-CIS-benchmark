from checks.templates.path_access import PathAccessRule, MultiPathsAccessRule
from checks.templates.file_content import NoSystemInformationRule

from pathlib import Path
import re

from utils import filesystem
from utils import ssh


def get_pam_motd_paths() -> list[str]:
    paths: list[str] = []
    pam_line = re.compile(
        r"^\s*session\s+(?:required|optional)\s+pam_motd\.so\b.*"
        r"\bmotd=(\"[^\"]+\"|'[^']+'|\S+)",
        re.IGNORECASE,
    )

    for service in ("sshd", "login", "su", "gdm-password"):
        candidates = (f"/etc/pam.d/{service}", f"/usr/lib/pam.d/{service}")
        pam_file = next((path for path in candidates if Path(path).is_file()), None)
        if pam_file is None:
            continue

        try:
            lines = filesystem.read_lines(pam_file)
        except OSError:
            continue

        for line in lines:
            match = pam_line.search(line)
            if match:
                path = match.group(1).strip("\"'")
                if path not in paths:
                    paths.append(path)

    return paths


def get_sshd_banner() -> str:
    return ssh.banner() or ""
