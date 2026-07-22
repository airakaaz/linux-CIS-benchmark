from ._Base_1_6 import NoSystemInformationRule


class Rule_1_6_1(NoSystemInformationRule):
    rule_id = "1.6.1"
    title = "Ensure /etc/motd is configured"
    server_lvl = 1
    workstation_lvl = 1

    _PATHS = (
        "/etc/motd",
        "/run/motd",
        "/usr/lib/motd",
        "/etc/motd.d/*",
        "/run/motd.d/*",
        "/usr/lib/motd.d/*",
        "/etc/update-motd.d/*",
    )
