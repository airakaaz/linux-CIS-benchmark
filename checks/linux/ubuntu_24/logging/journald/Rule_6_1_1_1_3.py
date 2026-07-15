from checks.templates.systemd_conf import SystemdConfOptionRule


class Rule_6_1_1_1_3(SystemdConfOptionRule):
    rule_id = "6.1.1.1.3"
    title = "Ensure journald is configured to send logs to rsyslog"
    _CONF_UNIT = "systemd/journald.conf"
    _SECTION = "Journal"
    _OPTION = "ForwardToSyslog"
    _ALLOW = {"yes"}
    _REQUIRED_PACKAGE = "rsyslog"
