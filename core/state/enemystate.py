from enum import Enum,auto

class ENEMYSTATE(Enum):
    IDLE = auto()
    PURSUING = auto()
    PATROLLING = auto()
    ATTACKING = auto()
    DEAD = auto()
    DETECTED = auto()