from ._Base_2_4_1 import AllowDenyFileRule


class Rule_2_4_2_1(AllowDenyFileRule):
    rule_id = "2.4.2.1"
    title = "Ensure at is restricted to authorized users"
    _PACKAGE = "at"
    _ALLOW_FILE = "/etc/at.allow"
    _DENY_FILE = "/etc/at.deny"
    _MAX_ACCESS = 0o640
    _VALID_OWNER_NAMES = {"root"}
    _VALID_GROUP_NAMES = {"root", "daemon"}
