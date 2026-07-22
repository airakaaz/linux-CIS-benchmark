from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_8(AccountDatabaseRule):
    rule_id = "7.2.8"
    title = "Ensure no duplicate group names exist"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(lambda: accounts.duplicate_accounts(0, "group name"))
    _EXPECTED = "all group names are unique"
