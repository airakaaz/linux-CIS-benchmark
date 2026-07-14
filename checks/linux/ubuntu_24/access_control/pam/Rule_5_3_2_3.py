from ._Base_5_3_2 import RequireFileContentRule


class Rule_5_3_2_3(RequireFileContentRule):
    rule_id = "5.3.2.3"
    title = "Ensure pam_pwquality module is enabled"

    _PATHS = [
        "/etc/pam.d/common-password",
    ]
    _PATTERN = r"\bpam_pwquality\.so\b"
