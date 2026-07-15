from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_2_6(PamPolicyRule):
    rule_id = "5.3.3.2.6"
    title = "Ensure password dictionary check is enabled"
    _CHECK = staticmethod(lambda: pam.pwquality_not_zero("dictcheck"))
    _EXPECTED = "dictcheck is not 0"
