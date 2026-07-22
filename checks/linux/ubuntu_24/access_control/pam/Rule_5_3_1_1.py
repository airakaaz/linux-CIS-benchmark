from ._Base_5_3_1 import VerifyInstalledRule


class Rule_5_3_1_1(VerifyInstalledRule):
    rule_id = "5.3.1.1"
    title = "Ensure latest version of pam is installed"
    workstation_lvl = 1
    server_lvl = 1

    _PACKAGES = {"libpam-runtime"}
    _VERIFY_UPTODATE = True
