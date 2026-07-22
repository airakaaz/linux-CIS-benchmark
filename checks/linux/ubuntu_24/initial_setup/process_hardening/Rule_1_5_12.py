from ._Base_1_5 import SystemdConfOptionRule


class Rule_1_5_12(SystemdConfOptionRule):
    rule_id = "1.5.12"
    title = "Ensure systemd-coredump Storage is configured"
    server_lvl = 1
    workstation_lvl = 1

    _CONF_UNIT = "systemd/coredump.conf"
    _SECTION = "Coredump"
    _OPTION = "Storage"
    _ALLOW = {"none"}
    _REQUIRED_PACKAGE = "systemd-coredump"
