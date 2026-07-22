from glob import glob
import re

from ._Base_1_6 import MultiPathsAccessRule


MOTD_RE = re.compile(r"motd=(\S+)")


def get_motd_paths() -> list[str]:
    paths: set[str] = set()

    for pam_file in glob("/etc/pam.d/*"):
        try:
            with open(pam_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    match = MOTD_RE.search(line)
                    if match:
                        paths.add(match.group(1))
        except OSError:
            continue

    return sorted(paths)


class Rule_1_6_9(MultiPathsAccessRule):
    rule_id = "1.6.9"
    title = "Ensure access to pam_motd file is configured"
    server_lvl = 1
    workstation_lvl = 1

    _MAX_ACCESS = 0o644
    _PATHS = get_motd_paths()
