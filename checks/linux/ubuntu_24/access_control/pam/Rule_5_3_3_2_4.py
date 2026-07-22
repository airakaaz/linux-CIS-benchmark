from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_2_4(PamPolicyRule):
    rule_id = "5.3.3.2.4"
    title = "Ensure password same consecutive characters is configured"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(lambda: pam.pwquality_numeric("maxrepeat", 1, 3))
    _EXPECTED = "maxrepeat is 1 through 3"
