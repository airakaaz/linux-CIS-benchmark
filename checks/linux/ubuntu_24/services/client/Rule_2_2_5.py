from ._Base_2_2 import VerifyNotInstalledRule


class Rule_2_2_5(VerifyNotInstalledRule):
    rule_id = "2.2.5"
    _PACKAGES = {"ldap-utils"}
    title = "Ensure ldap client is not installed"
