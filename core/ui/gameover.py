import pygame
from core.ui.button import Button

class GameOverMenu:
    def __init__(self, app, restart_callback, go_to_menu_callback, quit_callback):
        self.window = app
        self.screen = app.screen
        self.buttons = []
        self.restart_callback = restart_callback
        self.go_to_menu_callback = go_to_menu_callback
        self.quit_callback = quit_callback

        self.create_buttons()

    def create_buttons(self):
        self.buttons = [
            Button("Restart", 100, 150, 160, 50, (200, 50, 50), (255, 255, 255), self.restart_callback),
            Button("Menu", 100, 225, 160, 50, (200, 50, 50), (255, 255, 255), self.go_to_menu_callback),
            Button("Exit", 100, 300, 160, 50, (200, 50, 50), (255, 255, 255), self.quit_callback),
        ]

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        # Optional: Draw "GAME OVER" text
        font = self.window.font
        text = font.render("GAME OVER", True, (255, 0, 0))
        rect = text.get_rect(center=(self.window.width // 2, 80))
        self.screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.restart_callback()
        if event.type == pygame.QUIT:
            pygame.quit()
