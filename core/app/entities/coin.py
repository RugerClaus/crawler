import pygame
from core.app.entities.entity import Entity
from core.app.entities.animate import Animation

class Coin(Entity):
    def __init__(self, screen, grid_x, grid_y, tile_size, animation_frames=None, coin_type="gold"):
        super().__init__(screen, solid=False, health=1)
        
        self.coin_type = coin_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        
        self.rect = pygame.Rect(
            grid_x * tile_size,
            grid_y * tile_size,
            tile_size, tile_size
        )

        # Use provided animation frames, or fall back to an empty list if none are given
        animation_frames = animation_frames or []
        
        if animation_frames:  # Only set animation if frames are provided
            self.set_animation("spin", Animation(animation_frames, frame_delay=10))  
            self.play_animation("spin")
        else:
            print(f"[WARNING] Coin animation frames are empty for coin at ({grid_x}, {grid_y}).")

        self.value = self.set_coin_value(coin_type)

    def set_coin_value(self, coin_type):
        coin_values = {
            "gold": 100,
            "silver": 50,
            "bronze": 10,
        }
        return coin_values.get(coin_type, 0)

    def update_animation(self):
        super().update_animation()  # built-in from Entity

    def draw(self, camera):
        super().draw(camera)  # no need to repeat logic!

    def to_dict(self):
        # Serialize Coin specific attributes
        data = super().to_dict()  # Get base entity data
        data.update({
            "grid_x": self.grid_x,
            "grid_y": self.grid_y,
            "coin_type": self.coin_type,
            "value": self.value
        })
        return data
