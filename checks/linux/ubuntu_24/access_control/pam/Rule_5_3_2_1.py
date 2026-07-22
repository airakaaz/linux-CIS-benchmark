from ._Base_5_3_2 import RequireFileContentRule


class Rule_5_3_2_1(RequireFileContentRule):
    rule_id = "5.3.2.1"
    title = "Ensure pam_unix module is enabled"
    workstation_lvl = 1
    server_lvl = 1

    _PATHS = [
        "/etc/pam.d/common-account",
        "/etc/pam.d/common-auth",
        "/etc/pam.d/common-password",
        "/etc/pam.d/common-session",
        "/etc/pam.d/common-session-noninteractive",
    ]
    _PATTERN = r"\bpam_unix\.so\b"
