import pygame
from core.app.font import FontEngine

class Button:
    def __init__(self, text, x, y, width, height, text_unhovered_color, text_hovered_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = FontEngine("button").font
        self.action = action
        self.text_unhovered_color = text_unhovered_color
        self.text_hovered_color = text_hovered_color
        self.color = "black"

        self.surface = pygame.Surface((self.width, self.height))
        self.text_surface = self.font.render(self.text, True, self.text_unhovered_color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            text_color = self.text_hovered_color
        else:
            text_color = self.text_unhovered_color

        self.text_surface = self.font.render(self.text, True, text_color)

        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        # Debugging: print to check if button is clicked
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            print(f"Button {self.text} clicked!")  # Debugging
            if self.action:
                self.action()
