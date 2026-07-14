from checks.templates.systemd_conf import SystemdConfOptionRule


class Rule_6_1_1_1_6(SystemdConfOptionRule):
    rule_id = "6.1.1.1.6"
    _CONF_UNIT = "systemd/journald.conf"
    _SECTION = "Journal"
    _OPTION = "Storage"
    _ALLOW = {"persistent"}
    title = f"Ensure journald {_OPTION} is configured"
