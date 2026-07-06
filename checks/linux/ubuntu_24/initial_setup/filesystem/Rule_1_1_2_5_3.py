from ._Base_1_1_2 import MountOptionRule


class Rule_1_1_2_5_3(MountOptionRule):
    rule_id = "1.1.2.5.3"
    _MOUNT_POINT = "/var/tmp"
    _OPTION = "nosuid"
    title = f"Ensure {_OPTION} option set on {_MOUNT_POINT} partition"
