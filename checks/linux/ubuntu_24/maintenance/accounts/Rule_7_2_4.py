from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_4(AccountDatabaseRule):
    rule_id = "7.2.4"
    title = "Ensure shadow group is empty"
    _CHECK = staticmethod(accounts.shadow_group_issues)
    _EXPECTED = "shadow group has no members and is not a primary user group"
