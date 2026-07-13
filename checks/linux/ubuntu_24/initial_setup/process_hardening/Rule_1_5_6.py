from templates.verify_installed import VerifyNotInstalledRule


class Rule_1_5_6(VerifyNotInstalledRule):
    rule_id = "1.5.6"
    title = "Ensure prelink is not installed"

    _PACKAGES = {"prelink"}
