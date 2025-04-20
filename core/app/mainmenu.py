import pygame
import math
from core.ui.button import Button
from core.app.entities.animate import Animation

class MainMenu:
    def __init__(self, window, new_game_callback, load_callback, quit_calback):
        self.window = window
        self.screen = window.screen

        bg_frames = [
            pygame.image.load(f"assets/graphics/menu/menu_bg/frame_{i}.png").convert_alpha()
            for i in range(1, 15)
        ]
        self.background_animation = Animation(bg_frames, frame_delay=3)

        self.buttons = [
            Button("New Game", 600, 400, 200, 50, (255, 255, 255), (200, 200, 0), new_game_callback),
            Button("Load Game", 600, 500, 200, 50, (255, 255, 255), (200, 200, 0), load_callback),
            Button("Quit", 600, 600, 200, 50, (255, 255, 255), (200, 200, 0), quit_calback)
        ]

        self.title_image = pygame.image.load("assets/graphics/game/title.png").convert_alpha()
        self.title_rect = self.title_image.get_rect(center=(self.screen.get_width() // 2, 200))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)

    def update(self):
        self.background_animation.update()

    def draw(self):
        # Calculate pulsing color
        time = pygame.time.get_ticks() / 1000  # Smooth pulse over time
        pulse = (math.sin(time) + 1) / 2  # Range from 0 to 1

        # Define black and purple
        black = (20, 0, 20)
        purple = (35, 0, 35)  # You can tweak this for more or less purple

        # Interpolate between black and purple
        fade_color = (
            int(black[0] + (purple[0] - black[0]) * pulse),
            int(black[1] + (purple[1] - black[1]) * pulse),
            int(black[2] + (purple[2] - black[2]) * pulse)
        )

        self.screen.fill(fade_color)  # Set the pulsing background color

        # Draw background animation (over the fill)
        current_bg = self.background_animation.get_current_frame()
        self.screen.blit(current_bg, (250, -215))

        # Draw title and buttons
        self.screen.blit(self.title_image, self.title_rect)
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)
