from enum import Enum,auto

class GAMESTATE(Enum):
    PLAYER_INTERACTING = auto()
    PAUSED = auto()
    CUTSCENE = auto()

