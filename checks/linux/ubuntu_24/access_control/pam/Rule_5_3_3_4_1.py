from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_4_1(PamPolicyRule):
    rule_id = "5.3.3.4.1"
    title = "Ensure pam_unix does not include nullok"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(lambda: pam.pam_unix_absent("nullok"))
    _EXPECTED = "nullok is absent from pam_unix module lines"
