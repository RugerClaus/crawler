import pygame
import math
from core.app.font import FontEngine

class PlayerUI:

    def __init__(self, app):
        self.surface = pygame.surface.Surface((150, app.screen.get_height()), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.app = app
        self.font = FontEngine("UI").font
        self.font2 = FontEngine("default").font
        self.player = self.app.player
        self.health_potion_image = pygame.image.load("assets/graphics/game/items/potion/health_potion.png").convert_alpha()
        self.potion_rect = self.health_potion_image.get_rect(center=(25,300))
        self.ui_border = pygame.surface.Surface((10,self.rect.height))
        self.ui_border_rect = self.ui_border.get_rect(topleft = (140,0))
        self.potion_warning_start_time = None
        self.potion_text_color = (255,255,255)

    def draw(self, screen):
        if self.potion_warning_start_time is not None:
            now = pygame.time.get_ticks()
            elapsed = now - self.potion_warning_start_time

            if elapsed >= 200:
                self.potion_text_color = (255, 255, 255)  # Reset to white
                self.potion_warning_start_time = None
            else:
                # Linear interpolation between red and white
                t = elapsed / 500
                r = 255
                g = int(0 + t * (255 - 0))
                b = int(0 + t * (255 - 0))
                self.potion_text_color = (r, g, b)
        self.surface.fill((0, 0, 0, 0))
        self.draw_health_bar()
        self.surface.blit(self.ui_border,self.ui_border_rect)
        
        money_text = f"$: {self.player.money}"
        money_text_surface = self.font.render(money_text, True, (255, 255, 255))
        self.surface.blit(money_text_surface, (10, 10))

        health_text = f"Health: {self.player.current_health}/{self.player.max_health}"
        health_text_surface = self.font2.render(health_text, True, (255,255,255))
        self.surface.blit(health_text_surface, (10, 55))

        self.surface.blit(self.health_potion_image,self.potion_rect)
        health_potion_count_text = f" : {self.player.health_potion_count}/{self.player.health_potion_count_max}"
        health_potion_count_text_surface = self.font.render(health_potion_count_text,True,self.potion_text_color)
        self.surface.blit(health_potion_count_text_surface,(50,300))


        
        level_text = f"L: {self.app.world.level}"
        level_text_surface = self.font.render(level_text, True, (255, 255, 255))
        self.surface.blit(level_text_surface, (10, 700))
        
        screen.blit(self.surface, self.rect)

    def draw_health_bar(self):
        width, height = 25, 150
        health_ratio = self.player.current_health / self.player.max_health
        fill_height = health_ratio * height

        outline_rect = pygame.Rect(10, 75, width, height)
        fill_rect = pygame.Rect(
            10,
            75 + (height - fill_height),
            width,
            fill_height
        )

        if health_ratio <= 0.35:
            # Low health: pulse the color for attention
            time = pygame.time.get_ticks() / 500  # adjust speed here
            pulse = (math.sin(time) + 1) / 2  # smooth oscillation between 0 and 1

            dark = (150, 0, 0)
            bright = (255, 50, 50)
            fill_color = (
                int(dark[0] + (bright[0] - dark[0]) * pulse),
                int(dark[1] + (bright[1] - dark[1]) * pulse),
                int(dark[2] + (bright[2] - dark[2]) * pulse)
            )
        else:
            # Healthy: blend from green to red based on health level
            fill_color = (
                int(255 * (1 - health_ratio)),  # Red increases as health decreases
                int(255 * health_ratio),        # Green decreases as health decreases
                0                               # Blue stays 0
            )

        pygame.draw.rect(self.surface, fill_color, fill_rect)
        pygame.draw.rect(self.surface, (255, 255, 255), outline_rect, 2)
