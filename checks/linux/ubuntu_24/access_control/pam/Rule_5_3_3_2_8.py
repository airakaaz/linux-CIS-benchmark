from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_2_8(PamPolicyRule):
    rule_id = "5.3.3.2.8"
    title = "Ensure password quality is enforced for the root user"
    _CHECK = staticmethod(lambda: pam.pwquality_flag("enforce_for_root"))
    _EXPECTED = "enforce_for_root is enabled"
