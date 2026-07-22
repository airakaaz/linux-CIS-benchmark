from ._Base_6_2_4 import AUDIT_TOOLS, AuditdAccessRule


class Rule_6_2_4_9(AuditdAccessRule):
    rule_id = "6.2.4.9"
    title = "Ensure audit tools owner is configured"
    workstation_lvl = 2
    server_lvl = 2

    def check(self):
        return self.build_result(
            paths=list(AUDIT_TOOLS),
            valid_owners={0},
            expected="audit tools owned by root",
        )
