from enum import Enum,auto

class APPSTATE(Enum):
    MAIN_MENU = auto()
    GAME_ACTIVE = auto()
    GAME_OVER = auto()
    QUIT = auto()
    DEBUG = auto()