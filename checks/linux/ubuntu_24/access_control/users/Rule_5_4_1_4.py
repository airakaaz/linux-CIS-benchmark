from ._Base_5_4 import AccountPolicyRule, encrypt_method


class Rule_5_4_1_4(AccountPolicyRule):
    rule_id = "5.4.1.4"
    title = "Ensure strong password hashing algorithm is configured"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(encrypt_method)
    _EXPECTED = "ENCRYPT_METHOD is SHA512 or YESCRYPT"
