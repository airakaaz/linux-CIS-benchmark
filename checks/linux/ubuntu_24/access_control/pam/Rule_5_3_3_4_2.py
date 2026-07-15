from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_4_2(PamPolicyRule):
    rule_id = "5.3.3.4.2"
    title = "Ensure pam_unix does not include remember"
    _CHECK = staticmethod(lambda: pam.pam_unix_absent("remember"))
    _EXPECTED = "remember is absent from pam_unix module lines"
