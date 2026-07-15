from checks.templates.verify_installed import VerifyInstalledRule


class Rule_6_3_1(VerifyInstalledRule):
    rule_id = "6.3.1"
    title = "Ensure AIDE is installed"

    _PACKAGES = {"aide", "aide-common"}
