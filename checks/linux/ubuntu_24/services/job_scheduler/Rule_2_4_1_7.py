from ._Base_2_4_1 import DirectoryAccess


class Rule_2_4_1_7(DirectoryAccess):
    rule_id = "2.4.1.7"

    _PATH = "/etc/cron.yearly/"
    _MAX_ACCESS = 0o700

    title = f"Ensure access to {_PATH} is configured"
