from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_2_1(PamPolicyRule):
    rule_id = "5.3.3.2.1"
    title = "Ensure password number of changed characters is configured"
    _CHECK = staticmethod(lambda: pam.pwquality_numeric("difok", 2))
    _EXPECTED = "difok is 2 or greater"
