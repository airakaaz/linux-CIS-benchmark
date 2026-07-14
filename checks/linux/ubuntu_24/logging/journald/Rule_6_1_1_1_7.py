from checks.templates.systemd_conf import SystemdConfOptionRule


class Rule_6_1_1_1_7(SystemdConfOptionRule):
    rule_id = "6.1.1.1.7"
    _CONF_UNIT = "systemd/journald.conf"
    _SECTION = "Journal"
    _OPTION = "Compress"
    _ALLOW = {"yes"}
    title = f"Ensure journald {_OPTION} is configured"
