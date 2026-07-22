from checks.templates.verify_installed import VerifyInstalledRule


class Rule_1_3_1_1(VerifyInstalledRule):
    rule_id = "1.3.1.1"
    title = "Ensure apparmor packages are installed"
    server_lvl = 1
    workstation_lvl = 1

    _PACKAGES = {"apparmor", "apparmor-utils"}
