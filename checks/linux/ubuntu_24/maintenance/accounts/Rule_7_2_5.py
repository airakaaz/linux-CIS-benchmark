from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_5(AccountDatabaseRule):
    rule_id = "7.2.5"
    title = "Ensure no duplicate UIDs exist"
    _CHECK = staticmethod(lambda: accounts.duplicate_accounts(2, "UID"))
    _EXPECTED = "all UIDs are unique"
