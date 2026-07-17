from ._Base_7_1 import PathAccessRule
import grp


class Rule_7_1_7(PathAccessRule):
    rule_id = "7.1.7"

    _PATH = "/etc/gshadow"
    _MAX_ACCESS = 0o640
    _VALID_GROUPS = {0, grp.getgrnam("shadow").gr_gid}

    title = f"Ensure access to {_PATH} directory is configured"
