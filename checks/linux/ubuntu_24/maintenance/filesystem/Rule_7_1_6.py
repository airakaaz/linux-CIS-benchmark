from ._Base_7_1 import PathAccessRule


class Rule_7_1_6(PathAccessRule):
    rule_id = "7.1.6"

    _PATH = "/etc/shadow-"
    _MAX_ACCESS = 0o640

    title = f"Ensure access to {_PATH} directory is configured"
