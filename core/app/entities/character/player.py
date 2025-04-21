import pygame
from core.app.entities.entity import Entity
from core.app.entities.animate import Animation
from core.state.playerstate import PLAYERSTATE
from core.app.entities.items.coin import Coin
from core.app.entities.items.items import Item
from core.app.entities.items.healthpotion import HealthPotion
from core.app.entities.special_tiles.spike import Spike

class Player(Entity):
    def __init__(self, screen, world,x=1984,y=1984,health_potion_count=0,money=0,collected_items=list(),discarded_items=list()):
        super().__init__(screen, False, 0)
        self.world = world
        self.images = self.load_player_images()
        self.image = self.images["IDLE"][0]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y
        self.world_x = x
        self.world_y = y
        self.speed_x = 0
        self.speed_y = 0
        self.walking_speed = 5
        self.state = PLAYERSTATE.IDLE
        self.intent = PLAYERSTATE.IDLE
        self.set_animations()
        self.money = money
        self.current_health = 150
        self.max_health = 150
        self.game_over_state = False
        self.health_potion_count = health_potion_count
        self.health_potion_count_max = 5
        self.collected_items = collected_items
        self.discarded_items = discarded_items


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
            "DEAD": [pygame.image.load("assets/graphics/game/player/player_dead.png").convert_alpha()]
        }

    def set_animations(self):
        for key, frames in self.images.items():
            self.set_animation(key, Animation(frames, 10))

    def update(self, sound):
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

        if all(not self.world.is_blocked(tx, ty, sound) for tx, ty in horizontal_tiles):
            self.world_x = future_x

        # Then: check vertical movement
        vertical_tiles = [
            (self.world_x // self.world.tile_size, (future_y - half_h) // self.world.tile_size),
            (self.world_x // self.world.tile_size, (future_y + half_h - 1) // self.world.tile_size),
            ((self.world_x + half_w - 1) // self.world.tile_size, (future_y - half_h) // self.world.tile_size),
            ((self.world_x + half_w - 1) // self.world.tile_size, (future_y + half_h - 1) // self.world.tile_size),
        ]

        if all(not self.world.is_blocked(tx, ty, sound) for tx, ty in vertical_tiles):
            self.world_y = future_y

        self.rect.centerx = self.world_x
        self.rect.centery = self.world_y
        self.coords = (self.world_x, self.world_y)

        if self.current_health <= 0:
            self.state = PLAYERSTATE.DEAD
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
        elif self.state == PLAYERSTATE.DEAD:
            self.play_animation("DEAD")
        else:
            self.state = PLAYERSTATE.IDLE
            self.play_animation("IDLE")

    def update_movement(self):
        self.speed_x = 0
        self.speed_y = 0

        if self.intent == PLAYERSTATE.MOVING_RIGHT:
            self.state = PLAYERSTATE.MOVING_RIGHT
            self.speed_x = self.walking_speed
        elif self.intent == PLAYERSTATE.MOVING_LEFT:
            self.state = PLAYERSTATE.MOVING_LEFT
            self.speed_x = -self.walking_speed
        elif self.intent == PLAYERSTATE.MOVING_DOWN:
            self.state = PLAYERSTATE.MOVING_DOWN
            self.speed_y = self.walking_speed
        elif self.intent == PLAYERSTATE.MOVING_UP:
            self.state = PLAYERSTATE.MOVING_UP
            self.speed_y = -self.walking_speed
        else:
            self.state = PLAYERSTATE.IDLE

    def check_for_items(self,sound=None):
        for entity in self.world.entities:
            if isinstance(entity,Item):
                if self.rect.colliderect(entity.rect):
                    self.pick_up_item(entity,sound)
            else:
                pass

    def pick_up_item(self, item,sound):
        if isinstance(item,HealthPotion) and self.health_potion_count < self.health_potion_count_max:
            self.health_potion_count += 1
            item_props = {
                "item_id" : item.entity_id,
                "item_type": item.type,
                "heal_amount": item.heal_amount,
                "potion_type": item.potion_type
            }
            if sound is not None:
                sound("pickup_potion")
            self.collected_items.append(item_props)
            self.world.entities.remove(item)
        elif isinstance(item,Coin):
            self.money += item.value
            item_props = {
                "item_id": item.entity_id,
                "item_type": item.type,
                "coin_type": item.coin_type
            }
            if sound is not None:
                if item.coin_type == "gold": 
                    sound("gold_coin")
                if item.coin_type == "silver":
                    sound("silver_coin")
                if item.coin_type == "bronze":
                    sound("bronze_coin")
            self.collected_items.append(item_props)
            self.world.entities.remove(item)
        else:
            pass
        
        
    def check_for_damage_sources(self, entities, sound=None):
        for entity in entities:
            if isinstance(entity,Spike):
                if self.rect.colliderect(entity.rect):
                    
                    entity.hurt_player(self, sound)
            else:
                pass

    def use_health_potion(self, sound=None,ui=None):
        if self.current_health >= self.max_health:
            print("Can't heal past Max Health")
            return

        if self.health_potion_count == 0:
            if ui is not None:
                if ui.potion_warning_start_time is None:
                    ui.potion_warning_start_time = pygame.time.get_ticks()  # Start the timer
                    
                ui.potion_text_color = (255, 0, 0)  # Set red
                if sound is not None:
                    sound("no_more_item")
            print("No more potions")
            return

        for item_props in self.collected_items:
            if item_props["item_type"] == "health_potion":
                # Heal and clamp to max health
                self.current_health += item_props["heal_amount"]
                self.current_health = min(self.current_health, self.max_health)

                if sound is not None:
                    sound("drink_potion")

                # Update inventory and stats
                self.health_potion_count -= 1
                self.discarded_items.append(item_props)
                self.collected_items.remove(item_props)

                print("Used a health potion!")
                return

    def reset(self, world, x=1984, y=1984):
        self.world = world
        self.world_x = x
        self.world_y = y
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_x = 0
        self.speed_y = 0
        self.state = PLAYERSTATE.IDLE
        self.intent = PLAYERSTATE.IDLE
        self.money = 0
        self.current_health = 150
        self.game_over_state = False
        self.health_potion_count = 0
        self.collected_items.clear()
        self.discarded_items.clear()