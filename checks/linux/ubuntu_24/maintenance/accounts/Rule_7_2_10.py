from ._Base_7_2 import AccountDatabaseRule
from utils import accounts


class Rule_7_2_10(AccountDatabaseRule):
    rule_id = "7.2.10"
    title = "Ensure local interactive user dot files access is configured"
    workstation_lvl = 1
    server_lvl = 1
    _CHECK = staticmethod(accounts.interactive_dot_file_issues)
    _EXPECTED = "interactive dot files are protected and owned by the user and primary group"
