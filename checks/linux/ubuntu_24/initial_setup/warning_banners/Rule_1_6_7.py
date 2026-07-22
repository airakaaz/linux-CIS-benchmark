from ._Base_1_6 import MultiPathsAccessRule


class Rule_1_6_7(MultiPathsAccessRule):
    rule_id = "1.6.7"
    title = "Ensure access to /etc/issue is configured"
    server_lvl = 1
    workstation_lvl = 1

    _MAX_ACCESS = 0o644
    _PATHS = (
        "/etc/issue",
        "/usr/lib/issue.d/*",
        "/etc/issue.d/*",
        "/run/issue.d/*",
    )
