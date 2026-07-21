from core.module import Module

from .filesystem import filesystem
from .package_management import package_management
from .apparmor import apparmor
from .bootloader import bootloader
from .process_hardening import process_hardening
from .warning_banners import warning_banners
from .gdm import gdm

subMods = [
    filesystem,
    package_management,
    apparmor,
    bootloader,
    process_hardening,
    warning_banners,
    gdm,
]

initial_setup = Module(name="initial_setup", subMods=subMods)
