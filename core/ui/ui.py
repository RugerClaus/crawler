import pygame
from core.app.font import FontEngine

class UI:

    def __init__(self,app):
        self.surface = pygame.surface.Surface((100,400),pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.app = app
        self.font = FontEngine("UI").font
        self.player = self.app.player

    def draw(self,screen):
        
        self.surface.fill((0,0,0,0))
        money_text = f"$: {self.player.money}"
        money_text_surface = self.font.render(money_text,True,(255,255,255))
        self.surface.blit(money_text_surface,(10,10))
        screen.blit(self.surface,self.rect)