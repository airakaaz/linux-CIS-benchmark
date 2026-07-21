from core.module import Module

from .Rule_6_1_3_1 import Rule_6_1_3_1

rules = [
    Rule_6_1_3_1,
]

logfiles = Module(name="logfiles", rules=rules)
