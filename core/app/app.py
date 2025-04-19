import sys
import pygame
from core.app.entities.player import Player
from core.app.world.world import World
from core.app.world.camera import Camera
from core.state.playerstate import PLAYERSTATE
from core.sound.sound import SoundManager
from core.ui.pause import PauseMenu
from core.state.manager import StateManager
from core.state.appstate import APPSTATE
from core.state.gamestate import GAMESTATE
from core.app.mainmenu import MainMenu
from core.util.debugger import Debugger
from core.app.font import FontEngine
from core.ui.ui import UI
from core.ui.gameover import GameOverMenu

class Window():
    def __init__(self,version):
        self.width = 800
        self.height = 800
        self.version = version
        self.title = f"Crawler - Version: {self.version}"
        self.fps = 60
        pygame.init()
        
        self.font = FontEngine("default").font
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        self.state = StateManager()
        self.world = World(self.screen, 124,124, 32,1)
        self.world.generate_map()
        self.player = Player(self.screen, self.world)
        self.camera = Camera(self.width, self.height)  # Add this
        self.sound = SoundManager()
        self.pause_menu = PauseMenu(
            self,
            self.toggle_pause,
            self.toggle_music,
            self.toggle_sfx,
            self.go_to_menu,
            pygame.quit
        )
        self.game_over_menu = GameOverMenu(self,self.reset_game,self.go_to_menu,pygame.quit)
        self.pause_state = False
        self.main_menu = MainMenu(
        self,
        self.start_game,
        pygame.quit
        )
        self.ui = UI(self)
        self.debug = Debugger(self)
        self.debug_enabled = False
        pygame.display.set_caption(self.title)

    def start_game(self):
        self.sound.stop_music()
        self.state.set_app_state(APPSTATE.GAME_ACTIVE)
        self.sound.play_music("game")
    
    def reset_game(self):
        self.world = World(self.screen, 124, 124, 32, 1)  # Create a new world instance
        self.world.generate_map()
        self.player = Player(self.screen, self.world)  # Reset the player
        self.player.game_over_state = False
        self.player.current_health = self.player.max_health
        self.ui.player = self.player
        self.camera = Camera(self.width, self.height)  # Reset the camera
        self.state.set_game_state(GAMESTATE.PLAYER_INTERACTING)  # Ensure the game is active


    def go_to_menu(self):
        self.sound.stop_music()
        self.sound.play_music("menu")
        self.pause_state = False
        self.state.set_app_state(APPSTATE.MAIN_MENU)
        self.reset_game()
        

    def toggle_music(self):
        self.sound.toggle_music("game")
        self.pause_menu.update_labels()

    def toggle_sfx(self):
        self.sound.toggle_sfx()
        self.pause_menu.update_labels()

    def toggle_pause(self):
        self.pause_state = not self.pause_state

    def main_loop(self):
        self.state.set_app_state(APPSTATE.MAIN_MENU)
        self.sound.play_music("menu")  # Assuming you have a menu theme

        while True:
            self.handle_events()

            if self.state.is_app_state(APPSTATE.MAIN_MENU):
                self.main_menu.draw()
            elif self.state.is_app_state(APPSTATE.GAME_ACTIVE):
                if self.player.game_over_state:
                    self.game_over_menu.draw()
                elif self.pause_state:
                    self.state.set_game_state(GAMESTATE.PAUSED)
                    self.pause_menu.draw()
                else:
                    self.state.set_game_state(GAMESTATE.PLAYER_INTERACTING)
                    self.handle_input()
                    self.update_world_logic()
                    self.handle_collisions()
                    self.cleanup_entities()
                    self.draw_everything()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F9:
                    self.toggle_debug()

            if self.state.is_app_state(APPSTATE.MAIN_MENU):
                self.main_menu.handle_event(event)

            elif self.player.game_over_state:
                self.game_over_menu.handle_event(event)  # <-- Add this!

            elif self.state.is_game_state(GAMESTATE.PAUSED):
                self.pause_menu.handle_event(event)

            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.toggle_pause()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.intent = PLAYERSTATE.IDLE
        self.player.speed_x = 0
        self.player.speed_y = 0

        if keys[pygame.K_d]:
            self.player.intent = PLAYERSTATE.MOVING_RIGHT
        if keys[pygame.K_a]:
            self.player.intent = PLAYERSTATE.MOVING_LEFT
        if keys[pygame.K_s]:
            self.player.intent = PLAYERSTATE.MOVING_DOWN
        if keys[pygame.K_w]:
            self.player.intent = PLAYERSTATE.MOVING_UP
        
        #debug
        if keys[pygame.K_F5]:
            self.player.current_health -= 1

    def update_world_logic(self):
        self.player.update()
        for entity in self.world.entities:
            entity.update_animation()
        for tile in self.world.damaging_tiles:
            tile.hurt_player(self.player)

    def handle_collisions(self):
        self.player.check_for_coins(self.sound.play_sfx)
        self.player.check_for_damage_sources(self.world.entities,self.sound.play_sfx)

    def cleanup_entities(self):
        # Placeholder for when you want to remove dead or collected entities.
        pass

    def toggle_debug(self):
        self.debug_enabled = not self.debug_enabled

    def draw_everything(self):
        self.camera.update(self.player)
        self.screen.fill((0, 0, 0))
        self.world.draw(self.camera)
        self.player.draw(self.camera)
        self.world.draw_foreground(self.camera)
        self.ui.draw(self.screen)
        if self.debug_enabled == True:
            self.debug.draw(self.screen)