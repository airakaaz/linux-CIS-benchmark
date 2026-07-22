from checks.templates.path_access import PathAccessRule


class Rule_1_4_2(PathAccessRule):
    rule_id = "1.4.2"
    title = "Ensure access to bootloader config is configured"
    server_lvl = 1
    workstation_lvl = 1

    _MAX_ACCESS = 0o600
    _PATH = "/boot/grub/grub.cfg"
