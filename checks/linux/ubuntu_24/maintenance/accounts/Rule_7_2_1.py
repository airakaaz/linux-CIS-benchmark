from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_1(AccountDatabaseRule):
    rule_id = "7.2.1"
    title = "Ensure accounts in /etc/passwd use shadowed passwords"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(accounts.unshadowed_accounts)
    _EXPECTED = "all /etc/passwd password fields are x"
