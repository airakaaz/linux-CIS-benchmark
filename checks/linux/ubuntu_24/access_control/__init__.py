from . import pam, sudo

rules = []
rules.extend(pam.rules)
rules.extend(sudo.rules)
