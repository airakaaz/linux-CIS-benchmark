from ._Base_1_1_2 import MountOptionRule


class Rule_1_1_2_5_2(MountOptionRule):
    rule_id = "1.1.2.5.2"
    _MOUNT_POINT = "/var/tmp"
    _OPTION = "nodev"
    title = f"Ensure {_OPTION} option set on {_MOUNT_POINT} partition"
