from core.module import Module

from .journald import journald
from .rsyslog import rsyslog
from .logfiles import logfiles
from .auditd import auditd
from .integrity import integrity

subMods = [
    journald,
    rsyslog,
    logfiles,
    auditd,
    integrity,
]

logging = Module(name="logging", subMods=subMods)
