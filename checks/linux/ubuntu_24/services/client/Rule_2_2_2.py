from ._Base_2_2 import VerifyNotInstalledRule


class Rule_2_2_2(VerifyNotInstalledRule):
    rule_id = "2.2.2"
    _PACKAGES = {"rsh-client"}
    title = "Ensure rsh-client client is not installed"
    workstation_lvl = 1
    server_lvl = 1
