from ._Base_1_5 import SystemdConfOptionRule


class Rule_1_5_11(SystemdConfOptionRule):
    rule_id = "1.5.11"
    title = "Ensure systemd-coredump ProcessSizeMax is configured"

    _CONF_UNIT = "systemd/coredump.conf"
    _SECTION = "Coredump"
    _OPTION = "ProcessSizeMax"
    _ALLOW = {"0"}
