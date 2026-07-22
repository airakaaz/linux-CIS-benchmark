from ._Base_2_3 import EnabledServiceRule


class Rule_2_3_2_2(EnabledServiceRule):
    rule_id = "2.3.2.2"
    title = "Ensure systemd-timesyncd is enabled and active"
    workstation_lvl = 1
    server_lvl = 1
    _SERVICE = "systemd-timesyncd.service"
    _CHECK_ACTIVE = True
    _PACKAGE = "systemd-timesyncd"
