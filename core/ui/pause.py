# pause_menu.py

import pygame
from core.ui.button import Button
from core.app.font import FontEngine

class PauseMenu:
    def __init__(self, app, resume_callback, music_toggle_callback, sfx_toggle_callback, go_to_menu_callback, save_callback, quit_callback):
        self.window = app
        self.screen = app.screen
        self.buttons = []
        self.resume_callback = resume_callback
        self.music_toggle_callback = music_toggle_callback
        self.sfx_toggle_callback = sfx_toggle_callback
        self.go_to_menu_callback = go_to_menu_callback
        self.save_callback = save_callback
        self.quit_callback = quit_callback
        self.show_saving_message = False
        self.saving_message_start_time = 0
        self.font = FontEngine("button").font

        self.create_buttons()

    def create_buttons(self):
        self.buttons = [
            Button("Resume", 1000, 75, 170, 50, (173, 216, 230), (255, 255, 255), self.resume_callback),
            Button(f"Music: {self.window.sound.music_status()}", 1000, 150, 170, 50, (173, 216, 230), (255, 255, 255), self.music_toggle_callback),
            Button(f"SFX: {self.window.sound.sfx_status()}", 1000, 225, 170, 50, (173, 216, 230), (255, 255, 255), self.sfx_toggle_callback),
            Button(f"Menu", 1000, 300, 170, 50, (173, 216, 230), (255, 255, 255), self.go_to_menu_callback),
            Button(f"Save Game",1000,375,170,50,(173,216,230),(255,255,255),self.save_callback),
            Button("Exit", 1000, 450, 170, 50, (173, 216, 230), (255, 255, 255), self.quit_callback),
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.resume_callback()
        if event.type == pygame.QUIT:
            pygame.quit()

    