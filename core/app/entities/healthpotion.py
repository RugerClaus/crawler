import pygame
from core.app.entities.items import Item

class HealthPotion(Item):
    def __init__(self, screen, grid_x, grid_y, tile_size, potion_type="small", image=None, entity_id=None,item_type="health_potion"):
        super().__init__(screen, grid_x, grid_y, tile_size, item_id=f"healthpotion_{potion_type}", entity_id=entity_id,type=item_type)

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.type = item_type

        self.potion_type = potion_type
        self.heal_amount = self.set_heal_amount(potion_type)
        self.image = image

    def set_heal_amount(self, potion_type):
        potion_values = {
            "small": 25,
            "medium": 50,
            "large": 100
        }
        return potion_values.get(potion_type, 0)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "potion_type": self.potion_type,
            "heal_amount": self.heal_amount
        })
        return data
