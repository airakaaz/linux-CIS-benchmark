import re

from ._Base_6_2_1 import GrubAuditParameterRule


class Rule_6_2_1_3(GrubAuditParameterRule):
    rule_id = "6.2.1.3"
    title = "Ensure auditing for processes that start prior to auditd is enabled"
    _PARAMETER = "audit=1"
    _PATTERN = re.compile(r"\baudit=1\b")
