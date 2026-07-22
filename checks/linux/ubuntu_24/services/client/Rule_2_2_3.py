from ._Base_2_2 import VerifyNotInstalledRule


class Rule_2_2_3(VerifyNotInstalledRule):
    rule_id = "2.2.3"
    _PACKAGES = {"talk"}
    title = "Ensure talk client is not installed"
    workstation_lvl = 1
    server_lvl = 1
