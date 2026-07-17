from checks.templates.file_content import NoSystemInformationRule


class Rule_1_6_2(NoSystemInformationRule):
    rule_id = "1.6.2"
    title = "Ensure /etc/issue is configured"

    _PATHS = (
        "/etc/issue",
        "/usr/lib/issue.d/*",
        "/etc/issue.d/*",
        "/run/issue.d/*",
    )
