from . import pam, ssh, sudo

rules = []
rules.extend(pam.rules)
rules.extend(ssh.rules)
rules.extend(sudo.rules)
