from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_2_2(PamPolicyRule):
    rule_id = "5.3.3.2.2"
    title = "Ensure password length is configured"
    _CHECK = staticmethod(lambda: pam.pwquality_numeric("minlen", 14))
    _EXPECTED = "minlen is 14 or greater"
