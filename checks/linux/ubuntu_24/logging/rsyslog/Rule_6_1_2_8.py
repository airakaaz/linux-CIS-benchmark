from checks.templates.verify_installed import VerifyInstalledRule


class Rule_6_1_2_8(VerifyInstalledRule):
    rule_id = "6.1.2.8"
    title = "Ensure rsyslog-gnutls is installed"
    workstation_lvl = 2
    server_lvl = 2
    _PACKAGES = {"rsyslog-gnutls"}
