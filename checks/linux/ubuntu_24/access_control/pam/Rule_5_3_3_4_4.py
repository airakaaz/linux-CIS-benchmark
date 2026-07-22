from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_4_4(PamPolicyRule):
    rule_id = "5.3.3.4.4"
    title = "Ensure pam_unix includes use_authtok"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(lambda: pam.pam_unix_argument("use_authtok"))
    _EXPECTED = "use_authtok is present on pam_unix password lines"
