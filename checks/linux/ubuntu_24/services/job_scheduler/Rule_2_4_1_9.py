from ._Base_2_4_1 import AllowDenyFileRule


class Rule_2_4_1_9(AllowDenyFileRule):
    rule_id = "2.4.1.9"
    title = "Ensure access to crontab is configured"
    workstation_lvl = 1
    server_lvl = 1

    _PACKAGE = "cron"
    _ALLOW_FILE = "/etc/cron.allow"
    _DENY_FILE = "/etc/cron.deny"
    _MAX_ACCESS = 0o640
    _VALID_OWNER_NAMES = {"root"}
    _VALID_GROUP_NAMES = {"root", "crontab"}
