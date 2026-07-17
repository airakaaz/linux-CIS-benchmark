from ._Base_2_1 import PackageNotInstalledRule


class Rule_2_1_18(PackageNotInstalledRule):
    rule_id = "2.1.18"
    title = "Ensure snmp services are not in use"
    _PACKAGES = ("snmpd",)
    _MODE = "s"
    _ALLOW_AS_DEPENDENCY = True
    _SERVICES = ("snmpd.service",)
