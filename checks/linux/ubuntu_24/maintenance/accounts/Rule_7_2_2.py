from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_2(AccountDatabaseRule):
    rule_id = "7.2.2"
    title = "Ensure /etc/shadow password fields are not empty"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(accounts.empty_passwords)
    _EXPECTED = "no /etc/shadow password fields are empty"
