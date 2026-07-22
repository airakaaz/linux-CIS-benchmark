from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_1_3(PamPolicyRule):
    rule_id = "5.3.3.1.3"
    title = "Ensure password failed attempts lockout includes root account"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(pam.faillock_root)
    _EXPECTED = "even_deny_root or root_unlock_time is configured and root unlock time is at least 60 seconds"
