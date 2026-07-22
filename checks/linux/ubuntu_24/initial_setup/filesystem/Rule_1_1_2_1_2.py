from ._Base_1_1_2 import MountOptionRule


class Rule_1_1_2_1_2(MountOptionRule):
    rule_id = "1.1.2.1.2"
    _MOUNT_POINT = "/tmp"
    _OPTION = "nodev"
    title = f"Ensure {_OPTION} option set on {_MOUNT_POINT} partition"
    server_lvl = 1
    workstation_lvl = 1
