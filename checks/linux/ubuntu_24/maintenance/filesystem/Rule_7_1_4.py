from ._Base_7_1 import PathAccessRule


class Rule_7_1_4(PathAccessRule):
    rule_id = "7.1.4"

    _PATH = "/etc/group-"
    _MAX_ACCESS = 0o644

    title = f"Ensure access to {_PATH} directory is configured"
    workstation_lvl = 1
    server_lvl = 1
