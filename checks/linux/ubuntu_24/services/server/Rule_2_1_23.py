from checks.templates.verify_installed import VerifyNotInstalledRule


class Rule_2_1_23(VerifyNotInstalledRule):
    rule_id = "2.1.23"
    title = "Ensure X window server services are not in use"
    workstation_lvl = 0
    server_lvl = 2

    _PACKAGES = {"xserver-common"}
