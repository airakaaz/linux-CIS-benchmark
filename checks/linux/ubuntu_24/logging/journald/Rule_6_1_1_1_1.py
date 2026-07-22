from checks.templates.service_status import ActiveServiceRule


class Rule_6_1_1_1_1(ActiveServiceRule):
    rule_id = "6.1.1.1.1"
    title = "Ensure journald service is active"
    workstation_lvl = 1
    server_lvl = 1
    _SERVICE = "systemd-journald.service"
