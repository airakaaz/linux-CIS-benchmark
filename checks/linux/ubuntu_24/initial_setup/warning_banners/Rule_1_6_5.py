from checks.templates.file_content import NoSystemInformationRule

from ._Base_1_6 import get_sshd_banner


class Rule_1_6_5(NoSystemInformationRule):
    rule_id = "1.6.5"
    title = "Ensure sshd warning Banner is configured"
    server_lvl = 1
    workstation_lvl = 1

    def get_paths(self) -> list[str]:
        banner = get_sshd_banner()
        return [banner] if banner else []
