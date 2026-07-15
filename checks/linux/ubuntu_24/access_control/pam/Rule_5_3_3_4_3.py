from ._Base_5_3_3 import PamPolicyRule
from utils import pam


class Rule_5_3_3_4_3(PamPolicyRule):
    rule_id = "5.3.3.4.3"
    title = "Ensure pam_unix includes a strong password hashing algorithm"
    _CHECK = staticmethod(pam.pam_unix_hash)
    _EXPECTED = "pam_unix uses sha512 or yescrypt"
