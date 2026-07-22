import re

from ._Base_6_2_1 import GrubAuditParameterRule


class Rule_6_2_1_4(GrubAuditParameterRule):
    rule_id = "6.2.1.4"
    title = "Ensure audit_backlog_limit is configured"
    workstation_lvl = 2
    server_lvl = 2
    _PARAMETER = "audit_backlog_limit"
    _PATTERN = re.compile(r"\baudit_backlog_limit=\d+\b")
