from ._Base_1_1_2 import SeparatePartitionRule


class Rule_1_1_2_7_1(SeparatePartitionRule):
    _MOUNT_POINT = "/var/log/audit"

    rule_id = "1.1.2.7.1"
    title = f"Ensure separate partition exists for {_MOUNT_POINT}"
    server_lvl = 2
    workstation_lvl = 2
