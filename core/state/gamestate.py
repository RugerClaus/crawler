from enum import Enum,auto

class GAMESTATE(Enum):
    PLAYER_INTERACTING = auto()
    PAUSED = auto()
    CUTSCENE = auto()

class PLAYERSTATE(Enum):
    HOLDING_STILL = auto()
    FACING_LEFT = auto()
    FACING_RIGHT = auto()
    MOVING_LEFT = auto()
    MOVING_RIGHT = auto()
    JUMPING = auto()
    STUNNED = auto()

class ENEMYSTATE(Enum):
    pass