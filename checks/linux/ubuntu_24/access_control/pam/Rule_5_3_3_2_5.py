from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_2_5(PamPolicyRule):
    rule_id = "5.3.3.2.5"
    title = "Ensure password maximum sequential characters is configured"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(lambda: pam.pwquality_numeric("maxsequence", 1, 3))
    _EXPECTED = "maxsequence is 1 through 3"
