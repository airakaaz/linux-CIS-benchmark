from . import journald
from . import rsyslog
from . import auditd
from . import integrity
from .Rule_6_1_3_1 import Rule_6_1_3_1

rules = []
rules.extend(journald.rules)
rules.extend(rsyslog.rules)
rules.extend(auditd.rules)
rules.extend(integrity.rules)
rules.append(Rule_6_1_3_1)
