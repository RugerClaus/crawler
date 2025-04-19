import pygame
from core.app.entities.entity import Entity
from core.app.entities.animate import Animation
from core.state.playerstate import PLAYERSTATE
from core.app.entities.coin import Coin

class Player(Entity):
    def __init__(self, screen, world,x=1984,y=1984):
        super().__init__(screen, False, 0)
        self.world = world
        self.images = self.load_player_images()
        self.image = self.images["IDLE"][0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.world_x = self.rect.x
        self.world_y = self.rect.y
        self.speed_x = 0
        self.speed_y = 0
        self.state = PLAYERSTATE.IDLE
        self.intent = PLAYERSTATE.IDLE
        self.set_animations()
        self.money = 0
        self.current_health = 150
        self.max_health = 150
        self.game_over_state = False

    def load_player_images(self):
        return {
            "IDLE": [pygame.image.load("assets/graphics/game/player/player_stand.png").convert_alpha()],
            "MOVING_RIGHT": [
                pygame.image.load("assets/graphics/game/player/player_walk_1.png").convert_alpha(),
                pygame.image.load("assets/graphics/game/player/player_walk_2.png").convert_alpha()
            ],
            "MOVING_LEFT": [
                pygame.image.load("assets/graphics/game/player/player_walk_back_1.png").convert_alpha(),
                pygame.image.load("assets/graphics/game/player/player_walk_back_2.png").convert_alpha()
            ],
            "MOVING_UP": [
                pygame.image.load("assets/graphics/game/player/player_walk_up_1.png").convert_alpha(),
                pygame.image.load("assets/graphics/game/player/player_walk_up_2.png").convert_alpha()
            ],
            "MOVING_DOWN": [
                pygame.image.load("assets/graphics/game/player/player_walk_down_1.png").convert_alpha(),
                pygame.image.load("assets/graphics/game/player/player_walk_down_2.png").convert_alpha()
            ],
            "DEAD": [pygame.image.load("assets/graphics/game/player/player_dead.png")]
        }

    def set_animations(self):
        for key, frames in self.images.items():
            self.set_animation(key, Animation(frames, 10))

    def update(self):
        self.update_movement()

        future_x = self.world_x + self.speed_x
        future_y = self.world_y + self.speed_y

        half_w = self.rect.width // 2
        half_h = self.rect.height // 2

        # First: check horizontal movement
        horizontal_tiles = [
            ((future_x - half_w) // self.world.tile_size, self.world_y // self.world.tile_size),
            ((future_x + half_w - 1) // self.world.tile_size, self.world_y // self.world.tile_size),
            ((future_x - half_w) // self.world.tile_size, (self.world_y + half_h - 1) // self.world.tile_size),
            ((future_x + half_w - 1) // self.world.tile_size, (self.world_y + half_h - 1) // self.world.tile_size),
        ]

        if all(not self.world.is_blocked(tx, ty) for tx, ty in horizontal_tiles):
            self.world_x = future_x

        # Then: check vertical movement
        vertical_tiles = [
            (self.world_x // self.world.tile_size, (future_y - half_h) // self.world.tile_size),
            (self.world_x // self.world.tile_size, (future_y + half_h - 1) // self.world.tile_size),
            ((self.world_x + half_w - 1) // self.world.tile_size, (future_y - half_h) // self.world.tile_size),
            ((self.world_x + half_w - 1) // self.world.tile_size, (future_y + half_h - 1) // self.world.tile_size),
        ]

        if all(not self.world.is_blocked(tx, ty) for tx, ty in vertical_tiles):
            self.world_y = future_y

        self.rect.centerx = self.world_x
        self.rect.centery = self.world_y
        self.coords = (self.world_x, self.world_y)

        if self.current_health <= 0:
            self.health = 0
            self.game_over_state = True

        self.select_animation()
        self.update_animation()

    def select_animation(self):
        if self.state == PLAYERSTATE.MOVING_RIGHT:
            self.play_animation("MOVING_RIGHT")
        elif self.state == PLAYERSTATE.MOVING_LEFT:
            self.play_animation("MOVING_LEFT")
        elif self.state == PLAYERSTATE.MOVING_DOWN:
            self.play_animation("MOVING_DOWN")
        elif self.state == PLAYERSTATE.MOVING_UP:
            self.play_animation("MOVING_UP")
        else:
            self.state = PLAYERSTATE.IDLE
            self.play_animation("IDLE")

    def update_movement(self):
        self.speed_x = 0
        self.speed_y = 0

        if self.intent == PLAYERSTATE.MOVING_RIGHT:
            self.state = PLAYERSTATE.MOVING_RIGHT
            self.speed_x = 3
        elif self.intent == PLAYERSTATE.MOVING_LEFT:
            self.state = PLAYERSTATE.MOVING_LEFT
            self.speed_x = -3
        elif self.intent == PLAYERSTATE.MOVING_DOWN:
            self.state = PLAYERSTATE.MOVING_DOWN
            self.speed_y = 3
        elif self.intent == PLAYERSTATE.MOVING_UP:
            self.state = PLAYERSTATE.MOVING_UP
            self.speed_y = -3
        else:
            self.state = PLAYERSTATE.IDLE
    def check_for_coins(self,sound=None):
        for entity in self.world.entities:
            if isinstance(entity, Coin) and self.rect.colliderect(entity.rect):
                self.pick_up_coin(entity)
                if sound is not None:
                    if entity.coin_type == "gold": 
                        sound("gold_coin")
                    if entity.coin_type == "silver":
                        sound("silver_coin")
                    if entity.coin_type == "bronze":
                        sound("bronze_coin")

    def pick_up_coin(self, coin):
        # Increase score or add coin to inventory
        self.money += coin.value  # Add to score (or modify inventory if needed)
        print(f"Coin picked up! Current money: {self.money}")
        
        # Remove the coin from the world
        self.world.entities.remove(coin)  # <-- removes the coin from the world

    def check_for_damage_sources(self, entities,sound=None):
        for entity in entities:
            if self.rect.colliderect(entity.rect):
                entity.hurt_player(self,sound)