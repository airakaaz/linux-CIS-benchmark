from ._Base_2_4_1 import PathAccessRule


class Rule_2_4_1_2(PathAccessRule):
    rule_id = "2.4.1.2"

    _PATH = "/etc/crontab"
    _MAX_ACCESS = 0o600

    title = f"Ensure access to {_PATH} is configured"
