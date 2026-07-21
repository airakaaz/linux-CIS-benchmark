from core.module import Module

from .ssh import ssh
from .sudo import sudo
from .pam import pam
from .users import users

subMods = [
    ssh,
    sudo,
    pam,
    users,
]

access_control = Module(name="access_control", subMods=subMods)
