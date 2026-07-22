from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_2_7(PamPolicyRule):
    rule_id = "5.3.3.2.7"
    title = "Ensure password quality checking is enforced"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(lambda: pam.pwquality_not_zero("enforcing"))
    _EXPECTED = "enforcing is not 0"
