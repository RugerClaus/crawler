import pygame
from core.ui.button import Button  # assuming your Button class is in ui/button.py

class MainMenu:
    def __init__(self, window, start_game_action, quit_action):
        self.window = window
        self.screen = window.screen
        self.buttons = [
            Button("Start Game", 400, 300, 200, 50, (255,255,255), (200,200,0), start_game_action),
            Button("Quit", 400, 400, 200, 50, (255,255,255), (200,200,0), quit_action)
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)
