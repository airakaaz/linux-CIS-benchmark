from ._Base_2_2 import VerifyNotInstalledRule


class Rule_2_2_1(VerifyNotInstalledRule):
    rule_id = "2.2.1"
    _PACKAGES = {"nis"}
    title = "Ensure nis client is not installed"
    workstation_lvl = 1
    server_lvl = 1
