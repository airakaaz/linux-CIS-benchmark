from checks.templates.verify_installed import VerifyInstalledRule


class Rule_4_1_1(VerifyInstalledRule):
    rule_id = "4.1.1"
    title = "Ensure ufw is installed"
    workstation_lvl = 1
    server_lvl = 1

    _PACKAGES = {"ufw"}
