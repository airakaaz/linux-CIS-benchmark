from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_1_1(PamPolicyRule):
    rule_id = "5.3.3.1.1"
    title = "Ensure password failed attempts lockout is configured"
    _CHECK = staticmethod(pam.faillock_deny)
    _EXPECTED = "faillock deny is 1 through 5 and PAM overrides are not weaker"
