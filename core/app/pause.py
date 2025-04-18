# pause_menu.py

import pygame
from core.ui.button import Button

class PauseMenu:
    def __init__(self, app, resume_callback, music_toggle_callback, sfx_toggle_callback, go_to_menu_callback, quit_callback):
        self.window = app
        self.screen = app.screen
        self.buttons = []
        self.resume_callback = resume_callback
        self.music_toggle_callback = music_toggle_callback
        self.sfx_toggle_callback = sfx_toggle_callback
        self.go_to_menu_callback = go_to_menu_callback
        self.quit_callback = quit_callback

        self.create_buttons()

    def create_buttons(self):
        self.buttons = [
            Button("Resume", 100, 75, 160, 50, (173, 216, 230), (255, 255, 255), self.resume_callback),
            Button(f"Music: {self.window.sound.music_status()}", 100, 150, 160, 50, (173, 216, 230), (255, 255, 255), self.music_toggle_callback),
            Button(f"SFX: {self.window.sound.sfx_status()}", 100, 225, 160, 50, (173, 216, 230), (255, 255, 255), self.sfx_toggle_callback),
            Button(f"Menu", 100, 300, 160, 50, (173, 216, 230), (255, 255, 255), self.go_to_menu_callback),
            Button("Exit", 100, 375, 160, 50, (173, 216, 230), (255, 255, 255), self.quit_callback),
        ]

    def update_labels(self):
        self.buttons[1].text = f"Music: {self.window.sound.music_status()}"
        self.buttons[2].text = f"SFX: {self.window.sound.sfx_status()}"

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)  # True = left click
        if event.type == pygame.QUIT:
            pygame.quit()
