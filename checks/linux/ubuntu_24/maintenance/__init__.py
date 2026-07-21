from core.module import Module

from .filesystem import filesystem
from .accounts import accounts

subMods = [
    filesystem,
    accounts,
]

maintenance = Module(name="maintenance", subMods=subMods)
