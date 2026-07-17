import grp
from ._Base_7_1 import PathAccessRule


class Rule_7_1_5(PathAccessRule):
    rule_id = "7.1.5"

    _PATH = "/etc/shadow"
    _MAX_ACCESS = 0o640
    _VALID_GROUPS = {0, grp.getgrnam("shadow").gr_gid}

    title = f"Ensure access to {_PATH} directory is configured"
