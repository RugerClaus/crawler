import pygame
from core.app.entities.entity import Entity

class Item(Entity):
    def __init__(self, screen, grid_x, grid_y, tile_size, item_id, entity_id,type):
        super().__init__(screen, solid=False, health=1)
        self.item_id = item_id  # Type of item (coin, potion, etc.)
        self.entity_id = entity_id  # Unique instance ID
        self.type = type

        self.rect = pygame.Rect(
            grid_x * tile_size,
            grid_y * tile_size,
            tile_size, tile_size
        )

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "item_id": self.item_id,
            "grid_x": self.rect.x,
            "grid_y": self.rect.y,
            "collected": self.collected
        }