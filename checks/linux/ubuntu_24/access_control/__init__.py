from . import ssh
from . import sudo
from . import pam
from . import users

rules = []
rules.extend(ssh.rules)
rules.extend(sudo.rules)
rules.extend(pam.rules)
rules.extend(users.rules)
