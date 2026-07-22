from ._Base_1_6 import MultiPathsAccessRule


class Rule_1_6_6(MultiPathsAccessRule):
    rule_id = "1.6.6"
    title = "Ensure access to /etc/motd is configured"
    server_lvl = 1
    workstation_lvl = 1

    _MAX_ACCESS = 0o644
    _PATHS = (
        "/etc/issue",
        "/usr/lib/issue.d/*",
        "/etc/issue.d/*",
        "/run/issue.d/*",
    )
