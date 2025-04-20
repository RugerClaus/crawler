from core.app.entities.items import Item
from core.app.entities.animate import Animation

class Coin(Item):
    def __init__(self, screen, grid_x, grid_y, tile_size, animation_frames=None, coin_type="gold",
                 entity_id=None):
        super().__init__(screen, grid_x, grid_y, tile_size, item_id=f"coin_{coin_type}", entity_id=entity_id)

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.coin_type = coin_type
        self.value = self.set_coin_value(coin_type)

        animation_frames = animation_frames or []
        if animation_frames:
            self.set_animation("spin", Animation(animation_frames, frame_delay=10))
            self.play_animation("spin")
        else:
            print(f"[WARNING] Coin animation frames are empty for coin at ({grid_x}, {grid_y}).")

    def set_coin_value(self, coin_type):
        coin_values = {
            "gold": 100,
            "silver": 50,
            "bronze": 10,
        }
        return coin_values.get(coin_type, 0)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "coin_type": self.coin_type,
            "value": self.value
        })
        return data
