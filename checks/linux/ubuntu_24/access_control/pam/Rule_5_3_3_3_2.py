from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_3_2(PamPolicyRule):
    rule_id = "5.3.3.3.2"
    title = "Ensure password history is enforced for the root user"
    _CHECK = staticmethod(lambda: pam.pwhistory_option("enforce_for_root"))
    _EXPECTED = "enforce_for_root is enabled"
