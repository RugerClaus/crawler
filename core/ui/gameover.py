import pygame
from core.ui.button import Button
from core.app.font import FontEngine
from core.ui.saveslotselector import SlotSelector

class GameOverMenu:
    def __init__(self, app, restart_callback, go_to_menu_callback, load_callback, quit_callback):
        self.window = app
        self.screen = app.screen
        self.buttons = []
        self.restart_callback = restart_callback
        self.go_to_menu_callback = go_to_menu_callback
        self.load_callback = load_callback
        self.quit_callback = quit_callback
        self.font = FontEngine("GameOver").font
        self.slot_selector = None

        self.create_buttons()

    def create_buttons(self):
        self.buttons = [
            Button("Restart", 150, 450, 175, 40, (200, 50, 50), (255, 255, 255), self.restart_callback),
            Button("Menu", 450, 450, 175, 40, (200, 50, 50), (255, 255, 255), self.go_to_menu_callback),
            Button("Load Game", 750, 450, 175, 40, (200,50,50),(255,255,255), self.open_slot_selector),
            Button("Exit", 1050, 450, 175, 40, (200, 50, 50), (255, 255, 255), self.quit_callback),
        ]

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        text = self.font.render("GAME OVER", True, (0,0,0))
        rect = text.get_rect(center=(self.window.width // 2 , 300))
        self.screen.blit(text, rect)
        if self.slot_selector:
            self.slot_selector.draw()


    def handle_event(self, event):
        if self.slot_selector:
            self.slot_selector.handle_event(event)  # Pass event to slot selector
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.is_clicked(mouse_pos, True)
            if event.type == pygame.QUIT:
                pygame.quit()

    def open_slot_selector(self):
        self.slot_selector = SlotSelector(
            window=self.window,
            mode='load',  # We're in the Main Menu, so we're loading
            callback=self.load_callback,
            close_callback=self.close_slot_selector
        )

    def close_slot_selector(self):
        self.slot_selector = None  # Close popup
