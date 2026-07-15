from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_7(AccountDatabaseRule):
    rule_id = "7.2.7"
    title = "Ensure no duplicate user names exist"
    _CHECK = staticmethod(lambda: accounts.duplicate_accounts(0, "user name"))
    _EXPECTED = "all user names are unique"
