from . import journald
from . import rsyslog
from . import auditd

rules = []
rules.extend(journald.rules)
rules.extend(rsyslog.rules)
rules.extend(auditd.rules)
