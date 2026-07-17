from ._Base_7_1 import PathAccessRule
from utils.accounts import shadow_group_ids


class Rule_7_1_5(PathAccessRule):
    rule_id = "7.1.5"

    _PATH = "/etc/shadow"
    _MAX_ACCESS = 0o640
    _VALID_GROUPS = shadow_group_ids()

    title = f"Ensure access to {_PATH} directory is configured"
