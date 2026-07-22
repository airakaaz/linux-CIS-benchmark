from ._Base_1_2_1 import PathAccessRule


class Rule_1_2_1_4(PathAccessRule):
    rule_id = "1.2.1.4"

    _PATH = "/etc/apt/trusted.gpg.d"
    _MAX_ACCESS = 0o775

    title = f"Ensure access to {_PATH} directory is configured"
    server_lvl = 1
    workstation_lvl = 2
