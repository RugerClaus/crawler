import pygame
from core.app.enitites.animate import Animation
from core.app.enitites.entity import Entity

class Coin(Entity):
    def __init__(self, screen, grid_x, grid_y, tile_size, animation, coin_type):
        super().__init__(screen, solid=False, health=1)
        self.coin_type = coin_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size

        # Set up position in world grid
        self.rect = pygame.Rect(
            grid_x * tile_size,
            grid_y * tile_size,
            tile_size, tile_size
        )

        # Attach animation
        self.set_animation("spin", animation)
        self.play_animation("spin")

        # Set the coin's value based on its type
        self.value = self.set_coin_value(coin_type)

    def set_coin_value(self, coin_type):
        coin_values = {
            "gold": 100,
            "silver": 50,
            "bronze": 10,
        }
        return coin_values.get(coin_type, 0)  # Default to 0 if the coin type is unknown

    def update_animation(self):
        super().update_animation()  # built-in from Entity

    def draw(self, camera):
        super().draw(camera)  # no need to repeat logic!
