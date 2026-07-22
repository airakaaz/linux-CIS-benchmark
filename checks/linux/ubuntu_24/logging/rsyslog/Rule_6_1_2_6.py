from ._Base_6_1_2 import RsyslogRemoteInputRule


class Rule_6_1_2_6(RsyslogRemoteInputRule):
    rule_id = "6.1.2.6"
    title = "Ensure rsyslog is not configured to receive logs from a remote client"
    workstation_lvl = 1
    server_lvl = 1
