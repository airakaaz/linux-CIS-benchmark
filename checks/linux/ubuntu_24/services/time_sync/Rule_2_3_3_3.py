from ._Base_2_3 import EnabledServiceRule


class Rule_2_3_3_3(EnabledServiceRule):
    rule_id = "2.3.3.3"
    title = "Ensure chrony is enabled and active"
    _SERVICE = "chrony.service"
    _CHECK_ACTIVE = True
    _PACKAGE = "chrony"
