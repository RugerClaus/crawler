import pygame

class Debugger:

    def __init__(self,app):
        self.surface = pygame.surface.Surface((400,150))
        self.rect = self.surface.get_rect()
        self.rect.right = 1200
        self.app = app
        self.player = app.player
        self.font = self.app.font
        

    def draw(self, screen):
        self.surface.fill((128, 128, 128))

        
        tile_x = self.player.world_x // 32  
        tile_y = self.player.world_y // 32

        
        game_version_text = f"Version: {self.app.version}"
        tile_coords_text = f"Player Tile: ({tile_x},{tile_y})"
        fps_text = f"FPS: {round(self.app.clock.get_fps())}"
        enemy_count_text = f"Enemies in world: {len(self.app.world.enemies)}"
        game_version_text_surface = self.font.render(game_version_text,True,(255,255,255))
        coords_text_surface = self.font.render(tile_coords_text, True, (255, 255, 255))
        fps_text_surface = self.font.render(fps_text,True,(255,255,255))
        enemy_count_text_surface = self.font.render(enemy_count_text,True,(255,255,255))
        self.surface.blit(game_version_text_surface,(10,10))
        self.surface.blit(coords_text_surface, (10, 30))
        self.surface.blit(fps_text_surface,(10,50))
        self.surface.blit(enemy_count_text_surface,(10,70))
        
        screen.blit(self.surface, self.rect)