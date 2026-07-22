from ._Base_1_1_2 import MountOptionRule


class Rule_1_1_2_4_3(MountOptionRule):
    rule_id = "1.1.2.4.3"
    _MOUNT_POINT = "/var"
    _OPTION = "nosuid"
    title = f"Ensure {_OPTION} option set on {_MOUNT_POINT} partition"
    server_lvl = 1
    workstation_lvl = 1
