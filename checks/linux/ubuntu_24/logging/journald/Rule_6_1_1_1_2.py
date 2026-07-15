from checks.templates.service_status import DisabledServiceRule


class Rule_6_1_1_1_2(DisabledServiceRule):
    rule_id = "6.1.1.1.2"
    title = "Ensure systemd-journal-remote service is not in use"
    _SERVICES = (
        "systemd-journal-remote.socket",
        "systemd-journal-remote.service",
    )
