from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_3_1(PamPolicyRule):
    rule_id = "5.3.3.3.1"
    title = "Ensure password history remember is configured"
    _CHECK = staticmethod(lambda: pam.pwhistory_option("remember", 24))
    _EXPECTED = "remember is 24 or greater"
