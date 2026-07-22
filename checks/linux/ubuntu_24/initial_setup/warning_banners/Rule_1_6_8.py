from ._Base_1_6 import PathAccessRule


class Rule_1_6_8(PathAccessRule):
    rule_id = "1.6.8"
    title = "Ensure access to /etc/issue.net is configured"
    server_lvl = 1
    workstation_lvl = 1

    _MAX_ACCESS = 0o644
    _PATH = "/etc/issue.net"
