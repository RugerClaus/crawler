import pygame

class Tile:
    def __init__(self, image_path, is_walkable=True,deals_damage=False,damage_amount=10):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.damage_amount = damage_amount
        self.rect = self.image.get_rect()
        self.is_walkable = is_walkable  # Determines if the player can walk on this tile
        self.does_damage = deals_damage

    def render(self, screen, x, y, tile_size):
        # Draw the tile at the specified position
        screen_x = x * tile_size
        screen_y = y * tile_size
        screen.blit(self.image, (screen_x, screen_y))

    def hurt_player(self, player):
        if self.does_damage and self.rect.colliderect(player.rect):
            now = pygame.time.get_ticks()
            if not hasattr(player, 'last_damage_time') or now - player.last_damage_time > 1000:  # 1 sec cooldown
                player.current_health -= self.damage_amount
                player.last_damage_time = now