from checks.templates.verify_installed import VerifyInstalledRule


class Rule_6_1_2_8(VerifyInstalledRule):
    rule_id = "6.1.2.8"
    title = "Ensure rsyslog-gnutls is installed"
    _PACKAGES = {"rsyslog-gnutls"}
