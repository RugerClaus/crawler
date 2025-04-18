from core.state.appstate import APPSTATE
from core.state.gamestate import *

class StateManager:
    def __init__(self, debug=True):
        self.app_state = APPSTATE.MAIN_MENU
        self.previous_app_state = None
        self.allowed_transitions = {
            APPSTATE.MAIN_MENU: [APPSTATE.GAME_ACTIVE,APPSTATE.QUIT],
            APPSTATE.GAME_ACTIVE: [APPSTATE.MAIN_MENU,APPSTATE.QUIT],
            APPSTATE.QUIT: []
        }
        self.debug = debug

        self.game_state = GAMESTATE.PLAYER_INTERACTING  # Default game substate
        self.player_state = PLAYERSTATE.HOLDING_STILL
        self.enemy_states = {}  # could map enemy IDs to states

    def set_app_state(self, new_state):
        if new_state == self.app_state:
            return
        if new_state in self.allowed_transitions.get(self.app_state, []):
            self.previous_app_state = self.app_state
            self.app_state = new_state
            if self.debug:
                print(f"[APPSTATE] {self.previous_app_state.name} >>> {self.app_state.name}")
        else:
            if self.debug:
                print(f"[APPSTATE ERROR] Invalid: {self.app_state.name} >>> {new_state.name}")

    def is_app_state(self, state):
        return self.app_state == state
    
    def is_game_state(self,game_state):
        return self.game_state == game_state

    def set_game_state(self, new_game_state):
        if self.app_state != APPSTATE.GAME_ACTIVE:
            if self.debug:
                print("[GAMESTATE ERROR] Can't set GAMESTATE outside of GAME_ACTIVE.")
            return
        self.game_state = new_game_state
        # if self.debug:
        #     print(f"[GAMESTATE] Now: {self.game_state.name}")

    def set_player_state(self, new_player_state):
        self.player_state = new_player_state
        # if self.debug:
        #     print(f"[PLAYERSTATE] Now: {self.player_state.name}")
