from utils import filesystem

from checks.templates.file_content import NoSystemInformationRule


class Rule_1_6_3(NoSystemInformationRule):
    rule_id = "1.6.3"
    title = "Ensure /etc/issue.net is configured"

    _PATHS = filesystem.resolve_paths("/etc/issue.net")
