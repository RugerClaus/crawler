import pygame
from core.app.entities.entity import Entity

class Spike(Entity):
    def __init__(self, screen, grid_x, grid_y, tile_size, damage=10):
        super().__init__(screen, solid=False, health=1)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.entity_id = "spike"
        self.tile_size = tile_size
        self.image = pygame.image.load("assets/graphics/game/ground/spike.png")
        self.damage = damage

        self.rect = pygame.Rect(
            grid_x * tile_size,
            grid_y * tile_size,
            tile_size, tile_size
        )

    def hurt_player(self, player,sound=None):
        now = pygame.time.get_ticks()
        if not hasattr(player, 'last_damage_time') or now - player.last_damage_time > 1000:  # 1 sec i-frame
            player.current_health -= self.damage
            player.last_damage_time = now
            print("Ouch!")
            if sound is not None:
                sound("player_hurt")

    def draw(self, camera):
        super().draw(camera)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "grid_x": self.grid_x,
            "grid_y": self.grid_y,
            "damage": self.damage
        })
        return data