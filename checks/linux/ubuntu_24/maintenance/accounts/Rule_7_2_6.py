from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_6(AccountDatabaseRule):
    rule_id = "7.2.6"
    title = "Ensure no duplicate GIDs exist"
    _CHECK = staticmethod(lambda: accounts.duplicate_accounts(2, "GID"))
    _EXPECTED = "all GIDs are unique"
