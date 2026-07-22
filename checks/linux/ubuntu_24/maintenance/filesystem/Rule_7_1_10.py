from checks.templates.path_access import MultiPathsAccessRule


class Rule_7_1_10(MultiPathsAccessRule):
    rule_id = "7.1.10"
    title = "Ensure access to /etc/security/opasswd is configured"
    workstation_lvl = 1
    server_lvl = 1
    _PATHS = ["/etc/security/opasswd", "/etc/security/opasswd.old"]
    _MAX_ACCESS = 0o600
