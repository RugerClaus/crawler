from enum import Enum, auto
class PLAYERSTATE(Enum):
    IDLE = auto()
    MOVING_UP = auto()
    MOVING_DOWN = auto()
    MOVING_LEFT = auto()
    MOVING_RIGHT = auto()
    DEAD = auto()