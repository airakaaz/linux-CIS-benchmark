from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_3_3(PamPolicyRule):
    rule_id = "5.3.3.3.3"
    title = "Ensure pam_pwhistory includes use_authtok"
    _CHECK = staticmethod(lambda: pam.pwhistory_option("use_authtok"))
    _EXPECTED = "use_authtok is enabled"
