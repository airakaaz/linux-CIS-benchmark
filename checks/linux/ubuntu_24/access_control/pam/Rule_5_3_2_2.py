from ._Base_5_3_2 import RequireFileContentRule


class Rule_5_3_2_2(RequireFileContentRule):
    rule_id = "5.3.2.2"
    title = "Ensure pam_faillock module is enabled"
    workstation_lvl = 1
    server_lvl = 1

    _PATHS = [
        "/etc/pam.d/common-auth",
        "/etc/pam.d/common-account",
    ]
    _PATTERN = r"\bpam_faillock\.so\b"
