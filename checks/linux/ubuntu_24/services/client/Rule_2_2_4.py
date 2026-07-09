from ._Base_2_2 import VerifyNotInstalledRule


class Rule_2_2_4(VerifyNotInstalledRule):
    rule_id = "2.2.4"
    _PACKAGES = {"telnet", "inetutils-telnet"}
    title = "Ensure telnet client is not installed"
