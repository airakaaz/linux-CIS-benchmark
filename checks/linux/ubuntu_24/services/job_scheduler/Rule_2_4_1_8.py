from ._Base_2_4_1 import PathAccessRule


class Rule_2_4_1_8(PathAccessRule):
    rule_id = "2.4.1.8"

    _PATH = "/etc/cron.d/"
    _MAX_ACCESS = 0o700

    title = f"Ensure access to {_PATH} is configured"
