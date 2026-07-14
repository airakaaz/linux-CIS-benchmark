from checks.templates.file_content import NoSystemInformationRule

from ._Base_1_6 import get_pam_motd_paths


class Rule_1_6_4(NoSystemInformationRule):
    rule_id = "1.6.4"
    title = "Ensure pam_motd is configured"

    def get_paths(self) -> list[str]:
        return get_pam_motd_paths()
