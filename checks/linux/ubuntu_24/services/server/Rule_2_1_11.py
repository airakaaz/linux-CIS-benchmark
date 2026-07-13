from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_11(PackageNotInstalledRule):
    rule_id = "2.1.11"
    title = "Ensure message access server services are not in use"
    _PACKAGES = ("dovecot-imapd", "dovecot-pop3d")
    _MODE = "s"
    _SERVICES = ("dovecot.socket", "dovecot.service")
