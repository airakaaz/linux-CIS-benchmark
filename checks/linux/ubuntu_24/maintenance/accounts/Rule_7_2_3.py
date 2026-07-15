from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_3(AccountDatabaseRule):
    rule_id = "7.2.3"
    title = "Ensure all groups in /etc/passwd exist in /etc/group"
    _CHECK = staticmethod(accounts.missing_primary_groups)
    _EXPECTED = "every primary GID in /etc/passwd exists in /etc/group"
