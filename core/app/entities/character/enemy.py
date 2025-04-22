import pygame
from core.app.entities.entity import Entity
from core.state.enemystate import ENEMYSTATE
import math

class Enemy(Entity):
    def __init__(self, screen, world, grid_x, grid_y, tile_size):
        super().__init__(screen, False, 0)

        self.tile_size = tile_size
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.world_x = self.grid_x * self.tile_size
        self.world_y = self.grid_y * self.tile_size

        self.world = world
        self.state = ENEMYSTATE.IDLE  # Initial state is IDLE
        self.intent = ENEMYSTATE.IDLE  # Set initial intent to IDLE
        self.speed_x = 2
        self.speed_y = 2
        self.walking_speed = 0
        self.health = 100
        self.damage = 15

        self.original_world_x = self.world_x
        self.patrol_range = 5 * tile_size
        self.direction = 1  # 1 means moving right, -1 means moving left

        self.animations = {
            ENEMYSTATE.IDLE: [pygame.image.load("assets/graphics/game/enemies/idle_1.png").convert_alpha(),
                              pygame.image.load("assets/graphics/game/enemies/idle_2.png").convert_alpha()],
            ENEMYSTATE.PATROLLING: [pygame.image.load("assets/graphics/game/enemies/idle_1.png").convert_alpha(),
                                    pygame.image.load("assets/graphics/game/enemies/idle_2.png").convert_alpha()],
            ENEMYSTATE.DETECTED: [pygame.image.load("assets/graphics/game/enemies/idle_1.png").convert_alpha(),
                                    pygame.image.load("assets/graphics/game/enemies/idle_2.png").convert_alpha()],
        }


        self.animation = self.animations[ENEMYSTATE.IDLE]
        self.animation_frame_index = 0
        self.animation_delay = 10
        self.animation_timer = 0
        self.image = self.animation[self.animation_frame_index]
        self.rect = self.image.get_rect()

        self.detected_bubble_frames = [
            pygame.image.load("assets/graphics/game/enemies/detected_bubble_1.png").convert_alpha(),
            pygame.image.load("assets/graphics/game/enemies/detected_bubble_2.png").convert_alpha(),
            pygame.image.load("assets/graphics/game/enemies/detected_bubble_3.png").convert_alpha(),
        ]
        self.detected_bubble_frame_index = 0
        self.detected_bubble_animation_timer = 0
        self.detected_bubble_animation_delay = 10  # frames before switching to the next frame

        self.detection_radius = 10 * tile_size
        self.detection_timer = 0
        self.detection_delay_threshold = 30  # 1 second if your game runs at 60 FPS
        self.previous_state = self.state


    def draw(self, camera):
        pixel_x = int(self.world_x - camera.offset_x)
        pixel_y = int(self.world_y - camera.offset_y)

        self.screen.blit(self.image, (pixel_x, pixel_y))

        if self.state == ENEMYSTATE.DETECTED:
            bubble_frame = self.detected_bubble_frames[self.detected_bubble_frame_index]
            bubble_x = pixel_x + self.image.get_width() // 2 - bubble_frame.get_width() // 2
            bubble_y = pixel_y - bubble_frame.get_height() - 5
            self.screen.blit(bubble_frame, (bubble_x, bubble_y))

    def update(self, player):
        self.previous_state = self.state

        if self.health <= 0:
            self.state = ENEMYSTATE.DEAD
            self.animation = self.animations.get(ENEMYSTATE.DEAD, self.animation)
            return

        self.target = player

        self.rect.x = self.world_x
        self.rect.y = self.world_y

        if self.detect_player(player):
            if self.state != ENEMYSTATE.PURSUING:
                if self.detection_timer >= self.detection_delay_threshold:
                    self.state = ENEMYSTATE.PURSUING
                else:
                    self.state = ENEMYSTATE.DETECTED
                    self.detection_timer += 1
            else:
                self.pursue_player(player)
        else:
            self.detection_timer = 0
            self.state = ENEMYSTATE.PATROLLING
            self.patrol()

        if self.previous_state != self.state:
            self.animation = self.animations.get(self.state, self.animation)
            self.animation_frame_index = 0
            self.animation_timer = 0
            if self.state == ENEMYSTATE.DETECTED:
                self.detected_bubble_frame_index = 0
                self.detected_bubble_animation_timer = 0

        self.update_animation()


    def detect_player(self, player):
        dx = self.world_x - player.world_x
        dy = self.world_y - player.world_y
        distance = math.hypot(dx, dy)

        if distance <= self.detection_radius:
            start_grid_x = int(self.world_x // self.tile_size)
            start_grid_y = int(self.world_y // self.tile_size)
            end_grid_x = int(player.world_x // self.tile_size)
            end_grid_y = int(player.world_y // self.tile_size)

            if self.world.has_line_of_sight(start_grid_x, start_grid_y, end_grid_x, end_grid_y):
                return True

        return False


        
    def pursue_player(self, player):
        dx = player.world_x - self.world_x
        dy = player.world_y - self.world_y
        distance = math.hypot(dx, dy)

        if distance != 0:
            self.world_x += (dx / distance) * self.speed_x
            self.world_y += (dy / distance) * self.speed_y

    def patrol(self):
        self.world_x += self.speed_x * self.direction

        if self.world_x > self.original_world_x + self.patrol_range:
            self.direction = -1  # reverse left
        elif self.world_x < self.original_world_x - self.patrol_range:
            self.direction = 1  # reverse right

    def update_animation(self):
        if self.state in self.animations:
            current_animation = self.animations[self.state]
            self.animation_timer += 1

            if self.animation_timer >= self.animation_delay:
                self.animation_frame_index = (self.animation_frame_index + 1) % len(current_animation)
                self.animation_timer = 0

            self.image = current_animation[self.animation_frame_index]

        if self.state == ENEMYSTATE.DETECTED:
            # Only advance the animation if it hasn't finished
            if self.detected_bubble_frame_index < len(self.detected_bubble_frames) - 1:
                self.detected_bubble_animation_timer += 1
                if self.detected_bubble_animation_timer >= self.detected_bubble_animation_delay:
                    self.detected_bubble_frame_index += 1
                    self.detected_bubble_animation_timer = 0

    def get_position(self):
        return (self.world_x, self.world_y)

    def attack(self,player,sound):
        now = pygame.time.get_ticks()
        if not hasattr(player, 'last_damage_time') or now - player.last_damage_time > 1000:  # 1 sec i-frame
            player.current_health -= self.damage
            player.last_damage_time = now
            print("Ouch!")
            if sound is not None:
                sound("player_hurt")