import pygame

class FontEngine():
    def __init__(self,type):
        pygame.font.init()
        self.type = type
        self.font = None
        if self.type == "button":
            self.button_font()
        else:
            self.default_font()

    def button_font(self):
        self.font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
        
    def default_font(self):
        self.font = pygame.font.Font('assets/font/Pixeltype.ttf', 25)