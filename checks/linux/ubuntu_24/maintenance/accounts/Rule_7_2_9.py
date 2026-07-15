from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_9(AccountDatabaseRule):
    rule_id = "7.2.9"
    title = "Ensure local interactive user home directories are configured"
    _CHECK = staticmethod(accounts.interactive_home_issues)
    _EXPECTED = "interactive user homes exist, are user-owned, and are mode 750 or more restrictive"
