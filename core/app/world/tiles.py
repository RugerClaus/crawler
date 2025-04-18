import pygame

class Tile:
    def __init__(self, image_path, is_walkable=True):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.is_walkable = is_walkable  # Determines if the player can walk on this tile

    def render(self, screen, x, y, tile_size):
        # Draw the tile at the specified position
        screen_x = x * tile_size
        screen_y = y * tile_size
        screen.blit(self.image, (screen_x, screen_y))
