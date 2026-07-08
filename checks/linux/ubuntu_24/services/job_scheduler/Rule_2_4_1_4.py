from ._Base_2_4_1 import DirectoryAccess


class Rule_2_4_1_4(DirectoryAccess):
    rule_id = "2.4.1.4"

    _PATH = "/etc/cron.daily/"
    _MAX_ACCESS = 0o700

    title = f"Ensure access to {_PATH} is configured"
