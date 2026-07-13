from ._Base_5_3_1 import VerifyInstalledRule


class Rule_5_3_1_3(VerifyInstalledRule):
    rule_id = "5.3.1.3"
    title = "Ensure latest version of libpam-pwquality is installed"

    _PACKAGES = {"libpam-pwquality"}
    _VERIFY_UPTODATE = True
