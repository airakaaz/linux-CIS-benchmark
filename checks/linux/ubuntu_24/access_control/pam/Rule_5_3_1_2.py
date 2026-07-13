from ._Base_5_3_1 import VerifyInstalledRule


class Rule_5_3_1_2(VerifyInstalledRule):
    rule_id = "5.3.1.2"
    title = "Ensure latest version of libpam-modules is installed"

    _PACKAGES = {"libpam-modules"}
    _VERIFY_UPTODATE = True
