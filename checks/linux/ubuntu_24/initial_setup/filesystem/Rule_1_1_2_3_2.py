from ._Base_1_1_2 import MountOptionRule


class Rule_1_1_2_3_2(MountOptionRule):
    rule_id = "1.1.2.3.2"
    _MOUNT_POINT = "/home"
    _OPTION = "nodev"
    title = f"Ensure {_OPTION} option set on {_MOUNT_POINT} partition"
