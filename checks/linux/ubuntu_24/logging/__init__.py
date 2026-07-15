from . import journald
from . import rsyslog
from . import auditd
from . import integrity

rules = []
rules.extend(journald.rules)
rules.extend(rsyslog.rules)
rules.extend(auditd.rules)
rules.extend(integrity.rules)
