from ._Base_5_3_1 import VerifyInstalledRule


class Rule_5_3_1_4(VerifyInstalledRule):
    rule_id = "5.3.1.4"
    title = "Ensure latest version of cracklib-runtime is installed"

    _PACKAGES = {"cracklib-runtime"}
    _VERIFY_UPTODATE = True
