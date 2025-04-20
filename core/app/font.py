import pygame

class FontEngine():
    def __init__(self,type):
        pygame.font.init()
        self.type = type
        self.font = None
        if self.type == "button":
            self.button_font()
        elif self.type == "UI":
            self.ui_font()
        elif self.type == "GameOver":
            self.game_over_font()
        else:
            self.default_font()

    def button_font(self):
        self.font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
        
    def ui_font(self):
        self.font = pygame.font.Font('assets/font/Pixeltype.ttf', 40)
    def game_over_font(self):
        self.font = pygame.font.Font('assets/font/Pixeltype.ttf', 120)

    def default_font(self):
        self.font = pygame.font.Font('assets/font/Pixeltype.ttf', 25)