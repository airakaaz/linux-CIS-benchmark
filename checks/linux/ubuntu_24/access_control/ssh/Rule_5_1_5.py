from ._Base_5_1 import SshBannerRule


class Rule_5_1_5(SshBannerRule):
    rule_id = "5.1.5"
    title = "Ensure sshd Banner is configured"
    workstation_lvl = 1
    server_lvl = 1
