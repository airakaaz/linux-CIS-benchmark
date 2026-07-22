from ._Base_1_1_2 import SeparatePartitionRule


class Rule_1_1_2_6_1(SeparatePartitionRule):
    _MOUNT_POINT = "/var/log"

    rule_id = "1.1.2.6.1"
    title = f"Ensure separate partition exists for {_MOUNT_POINT}"
    server_lvl = 2
    workstation_lvl = 2
