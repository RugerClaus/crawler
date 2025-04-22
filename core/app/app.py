import sys
import pygame
from core.app.entities.character.player import Player
from core.app.world.world import World
from core.app.world.camera import Camera
from core.state.playerstate import PLAYERSTATE
from core.sound.sound import SoundManager
from core.ui.pause import PauseMenu
from core.state.manager import StateManager
from core.state.appstate import APPSTATE
from core.state.gamestate import GAMESTATE
from core.state.enemystate import ENEMYSTATE
from core.app.mainmenu import MainMenu
from core.util.debugger import Debugger
from core.app.font import FontEngine
from core.ui.ui import PlayerUI as UI
from core.ui.gameover import GameOverMenu
from core.util.savemanager import SaveManager

class Window():
    def __init__(self,version):
        self.width = 1200
        self.height = 800
        self.version = version
        self.title = f"Crawler - Version: {self.version}"
        self.fps = 60
        pygame.init()
        self.save_manager = SaveManager(slot=1)
        self.font = FontEngine("default").font
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        self.state = StateManager()
        self.world = World(self.screen, 124,124, 32,1)
        self.player = Player(self.screen, self.world)
        self.world.generate_map(self.player)
        self.camera = Camera(self.width, self.height)
        self.sound = SoundManager()
        self.pause_menu = PauseMenu(
            self,
            self.toggle_pause,
            self.toggle_music,
            self.toggle_sfx,
            self.go_to_menu,
            self.save_game,
            pygame.quit
        )
        self.game_over_menu = GameOverMenu(self,self.reset_game,self.go_to_menu,self.load_game,pygame.quit)
        self.pause_state = False
        self.main_menu = MainMenu(
        self,
        self.start_game,
        self.load_game,
        pygame.quit
        )
        self.ui = UI(self)
        self.debug = Debugger(self)
        self.debug_enabled = False
        pygame.display.set_caption(self.title)
        self.saving_message_start_time = 0
        self.show_saving_message = False

    def toggle_saving_message(self):
        print(f"currently saving: {self.show_saving_message}")
        self.show_saving_message = not self.show_saving_message
        print(f"currently saving: {self.show_saving_message}")

    def start_game(self):
        self.sound.stop_music()
        self.state.set_app_state(APPSTATE.GAME_ACTIVE)

        if self.world is None:
            self.world = World(self.screen, 124, 124, 32, 1)
        else:
            self.world.reset()

        if self.player is None:
            self.player = Player(self.screen, self.world)
        else:
            self.player.reset(self.world)

        self.world.generate_map(self.player)

        self.sound.play_music("game")
        print(f"Starting new game, collected items,discarded items = {self.player.collected_items} || {self.player.discarded_items}")

    
    def save_game(self,slot):
        print("Saving game...")
        print(f"Entities before save: {len(self.world.entities)}")
        self.saving_message_start_time = pygame.time.get_ticks()
        self.toggle_saving_message()
        self.save_manager = SaveManager(slot)
        self.save_manager.save(self.player, self.world,self.version)
        print(f"Entities after save: {len(self.world.entities)}")
        self.pause_menu.close_slot_selector()
        
    def load_game(self,slot):
        self.sound.stop_sfx()
        self.state.set_app_state(APPSTATE.GAME_ACTIVE)
        self.state.set_game_state(GAMESTATE.PLAYER_INTERACTING)

        print("Loading save data...")
        self.save_manager = SaveManager(slot)
        self.save_manager.load(self.player, self.world,self.version)
        
        print(f"Loaded save data: {self.save_manager.loaded_data}")

        self.world = World(self.screen, 124, 124, 32, 1)
        
        saved_level = self.save_manager.loaded_data["level"]
        print(f"Loaded level: {saved_level}")
        
        self.world.level = saved_level
        
        print("Creating player object...")
        player_data = self.save_manager.loaded_data["player"]
        self.player = Player(self.screen, self.world, player_data["x"], player_data["y"],
                             player_data["potion_count"],player_data["money"],collected_items=player_data["collected_items"],
                             discarded_items=player_data["discarded_items"])
        self.world.generate_map(self.player)
        
        print(f"Setting player position and health: {player_data}")
        self.player.current_health = player_data["health"]

        print("Syncing UI and camera with player and world...")
        self.ui.player = self.player
        self.camera = Camera(self.width, self.height)

        print(f"Enemies in save: {self.save_manager.loaded_data.get('enemies', [])}")

        print("Changing music...")
        self.sound.stop_music()
        self.sound.play_music("game")



    def reset_game(self):
        self.sound.stop_sfx()
        self.world = World(self.screen, 124, 124, 32, 1) 
        self.world.generate_map(self.player)
        self.player = Player(self.screen, self.world) 
        self.player.game_over_state = False
        self.player.current_health = self.player.max_health
        self.ui.player = self.player
        self.camera = Camera(self.width, self.height) 
        self.state.set_game_state(GAMESTATE.PLAYER_INTERACTING) 
        self.sound.play_music("game")

    def draw_saving_text(self):
        if self.show_saving_message:
            now = pygame.time.get_ticks()
            elapsed = now - self.saving_message_start_time

            fade_duration = 500 
            visible_duration = 1000 

            if elapsed < visible_duration:
                alpha = 255 
            elif elapsed < visible_duration + fade_duration:
                
                fade_progress = (elapsed - visible_duration) / fade_duration
                alpha = int(255 * (1 - fade_progress))
            else:
                self.show_saving_message = False
                return 

            text_surface = self.font.render("Saving Game...", True, (255, 255, 255))
            text_surface.set_alpha(alpha)

            text_surface = text_surface.convert_alpha()

            self.screen.blit(text_surface, (50, 750))

    def go_to_menu(self):
        self.sound.stop_sfx()
        self.sound.stop_music()
        self.sound.play_music("menu")
        self.pause_state = False
        self.main_menu = MainMenu(
        self,
        self.start_game,
        self.load_game,
        pygame.quit
        )
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
        self.sound.play_music("menu")

        while True:
            self.handle_events()

            if self.state.is_app_state(APPSTATE.MAIN_MENU):
                self.main_menu.update()
                self.main_menu.draw()
            elif self.state.is_app_state(APPSTATE.GAME_ACTIVE):
                if self.player.game_over_state:
                    self.draw_everything()
                    self.game_over_menu.draw()
                    self.sound.stop_music()
                    self.sound.play_sfx("game_over")
                elif self.pause_state:
                    self.state.set_game_state(GAMESTATE.PAUSED)
                    self.draw_everything()
                    self.pause_menu.draw()
                    self.draw_saving_text()
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
                if event.key == pygame.K_F1:
                    self.world.generate_enemy()
                if event.key == pygame.K_g:
                    for enemy in self.world.enemies:
                        enemy.intent = ENEMYSTATE.PATROLLING
                        print(f"Setting enemy intent to PATROLLING: {enemy.intent}")
                if event.key == pygame.K_h:
                    for enemy in self.world.enemies:
                        enemy.intent = ENEMYSTATE.IDLE
                        print(f"Setting enemy intent to IDLE: {enemy.intent}")
                if event.key == pygame.K_1:
                    self.player.use_health_potion(self.sound.play_sfx,self.ui)        

            if self.state.is_app_state(APPSTATE.MAIN_MENU):
                self.main_menu.handle_event(event)

            elif self.player.game_over_state:
                self.game_over_menu.handle_event(event)

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
        self.player.update(self.sound.play_sfx)
        
        for entity in self.world.entities:
            entity.update_animation()
        for tile in self.world.damaging_tiles:
            tile.hurt_player(self.player)
        if not self.pause_state:
            for enemy in self.world.enemies:
                enemy.update(self.player,self.sound)
                enemy.check_health(self.sound.play_sfx)


    def handle_collisions(self):
        self.player.check_for_items(self.sound.play_sfx)
        self.player.check_for_damage_sources(self.world.entities,self.sound.play_sfx)
        self.player.check_for_enemies(self.world.enemies,self.sound.play_sfx)
        for enemy in self.world.enemies:
            enemy.check_for_damage_sources(self.world.entities,self.sound.play_sfx)

    def cleanup_entities(self):
        
        pass

    def toggle_debug(self):
        self.debug_enabled = not self.debug_enabled

    def draw_everything(self):
        self.camera.update(self.player)
        self.screen.fill((0, 0, 0))
        self.world.draw(self.camera)
        self.player.draw(self.camera)
        for enemy in self.world.enemies:
            enemy.draw(self.camera)
        
        self.world.draw_foreground(self.camera)
        self.ui.draw(self.screen)
        if self.debug_enabled == True:
            self.debug.draw(self.screen)
