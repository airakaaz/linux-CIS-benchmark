from ._Base_5_3_2 import RequireFileContentRule


class Rule_5_3_2_4(RequireFileContentRule):
    rule_id = "5.3.2.4"
    title = "Ensure pam_pwhistory module is enabled"

    _PATHS = [
        "/etc/pam.d/common-password",
    ]
    _PATTERN = r"\bpam_pwhistory\.so\b"
