from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_1_2(PamPolicyRule):
    rule_id = "5.3.3.1.2"
    title = "Ensure password unlock time is configured"
    workstation_lvl = 2
    server_lvl = 2
    _CHECK = staticmethod(pam.faillock_unlock_time)
    _EXPECTED = "unlock_time is 0 or at least 900 seconds"
