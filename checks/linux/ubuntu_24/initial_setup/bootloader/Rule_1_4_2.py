from checks.templates.directory_access import DirectoryAccess


class Rule_1_4_2(DirectoryAccess):
    rule_id = "1.4.2"
    title = "Ensure access to bootloader config is configured"

    _MAX_ACCESS = 0o600
    _PATH = "/boot/grub/grub.cfg"
