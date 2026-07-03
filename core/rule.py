from abc import ABC, abstractmethod
from enum import Enum

from core.result import ScanResult


class Mode(Enum):
    AUTOMATIC = 1
    MANUAL = 0


class CISRule(ABC):
    rule_id: str = ""
    title: str = ""
    mode: Mode = Mode.AUTOMATIC

    @abstractmethod
    def check(self) -> ScanResult:
        raise NotImplementedError
