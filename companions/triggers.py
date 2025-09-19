from enum import Enum, auto

class CompanionTrigger(Enum):
    PRE_FIGHT = auto()
    TURN_START = auto()
    TURN_END = auto()
    POST_FIGHT = auto()