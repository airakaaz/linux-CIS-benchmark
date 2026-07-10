from ._Base_1_2_1 import PathAccessRule


class Rule_1_2_1_6(PathAccessRule):
    rule_id = "1.2.1.6"

    _PATH = "/etc/apt/auth.conf.d"
    _MAX_ACCESS = 0o640

    title = f"Ensure access to {_PATH} directory is configured"
