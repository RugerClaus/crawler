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
        self.speed_y = 0
        self.walking_speed = 0
        self.health = 100

        self.original_world_x = self.world_x
        self.patrol_range = 10
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

        self.detected_bubble_frames = [
            pygame.image.load("assets/graphics/game/enemies/detected_bubble_1.png").convert_alpha(),
            pygame.image.load("assets/graphics/game/enemies/detected_bubble_2.png").convert_alpha(),
            pygame.image.load("assets/graphics/game/enemies/detected_bubble_3.png").convert_alpha(),
        ]
        self.detected_bubble_frame_index = 0
        self.detected_bubble_animation_timer = 0
        self.detected_bubble_animation_delay = 10  # frames before switching to the next frame

        self.detection_radius = 10 * tile_size

    def draw(self, camera):
        pixel_x = int(self.world_x - camera.offset_x)
        pixel_y = int(self.world_y - camera.offset_y)

        print(f"Enemy world position: ({self.world_x}, {self.world_y})")
        self.screen.blit(self.image, (pixel_x, pixel_y))

        if self.state == ENEMYSTATE.DETECTED:
            bubble_frame = self.detected_bubble_frames[self.detected_bubble_frame_index]
            bubble_x = pixel_x + self.image.get_width() // 2 - bubble_frame.get_width() // 2
            bubble_y = pixel_y - bubble_frame.get_height() - 5  # adjust offset for "above head"
            self.screen.blit(bubble_frame, (bubble_x, bubble_y))

    def update(self, player):
        if self.health <= 0:
            self.state = ENEMYSTATE.DEAD
            self.animation = self.animations[ENEMYSTATE.DEAD]
            return

        print(f"[Before] world: ({self.world_x},{self.world_y}) grid: ({self.grid_x},{self.grid_y})")
        self.target = player
        self.detect_player(player)
        self.apply_intent()  # Apply patrol logic based on current intent
        self.update_animation()
        print(f"[After] world: ({self.world_x},{self.world_y}) grid: ({self.grid_x},{self.grid_y})\n")

    def detect_player(self, player):
        dx = self.world_x - player.world_x
        dy = self.world_y - player.world_y
        distance = math.sqrt(dx**2 + dy**2)

        previous_state = self.state

        if distance <= self.detection_radius:
            self.state = ENEMYSTATE.DETECTED
            self.intent = ENEMYSTATE.DETECTED
            print(f"Player detected! Distance: {distance}")
        else:
            self.state = ENEMYSTATE.IDLE
            self.intent = ENEMYSTATE.IDLE

        if self.state != previous_state:
            self.animation_frame_index = 0
            self.animation_timer = 0
            if self.state in self.animations:
                self.animation = self.animations[self.state]

            if self.state == ENEMYSTATE.DETECTED:
                self.detected_bubble_frame_index = 0
                self.detected_bubble_animation_timer = 0

        print(f"Enemy at ({self.world_x}, {self.world_y}) -- Player at ({player.world_x}, {player.world_y}) -- Distance: {distance}")


    def apply_intent(self):
        print(f"Applying intent: {self.intent}")  # Debug to see if intent is applied

        if self.intent == ENEMYSTATE.PATROLLING:
            print(f"Moving enemy. Current position: {self.world_x}, Direction: {self.direction}")
            self.world_x += self.speed_x * self.direction  # Move in the current direction

            if self.world_x > self.original_world_x + self.patrol_range:
                self.direction = -1  # Reverse direction (move left)
            elif self.world_x < self.original_world_x - self.patrol_range:
                self.direction = 1  # Reverse direction (move right)

        elif self.intent == ENEMYSTATE.DETECTED:
            self.state = ENEMYSTATE.DETECTED

        elif self.intent == ENEMYSTATE.IDLE:
            self.world_x = self.world_x  # Stop moving if idle

        print(f"Intent: {self.intent}, Speed: ({self.speed_x}, {self.speed_y}), Direction: {self.direction}")

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
