import pygame
import os
from core.app.font import FontEngine
from core.ui.button import Button

class SlotSelector:
    def __init__(self, window, mode, callback, close_callback):

        self.window = window
        self.screen = window.screen
        self.mode = mode  # 'load' or 'save'
        self.callback = callback
        self.close_callback = close_callback
        self.buttons = []  # Store buttons for the slots
        self.font = FontEngine("button").font
        self.font2 = FontEngine("back").font
        x_offset = 75

        # Initialize the buttons for each slot
        for i in range(1, 4):
            self.slot = i
            filepath = f"saves/save_slot_{i}.json"
            exists = os.path.exists(filepath)

            # Adjust x and y to position the buttons
            x = 450 + (i - 1) * 220 - x_offset
            y = 350
            width, height = 200, 100

            # Determine the text and behavior based on mode and slot state
            button_text = f"Slot {i}"
            if self.mode == 'save' and exists:
                button_text = f"Slot {i}: \nOverwrite?"
            elif self.mode == 'load' and not exists:
                button_text = f"Slot {i}: (Empty)"

            # Create a Button for this slot, passing a wrapper function for the callback
            button = Button(
                text=button_text,
                x=x, y=y,
                width=width, height=height,
                text_unhovered_color=(255, 255, 255),
                text_hovered_color=(0, 255, 0),
                action=self.get_slot_callback(i)  # Use the wrapper function to handle the slot callback
            )

            # Set button as active if needed
            button.active = exists if self.mode == 'load' else True
            self.buttons.append(button)

    def get_slot_callback(self,slot):

        def slot_callback():
            print(f"Slot {slot} selected.")  # Debugging: print when the slot is clicked
            self.callback(slot)
            self.close_callback()
        return slot_callback

    def handle_event(self, event):
        # Handle mouse click and key press events for buttons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos) and button.active:
                    print(f"Button {button.text} clicked.")  # Debugging: print when a button is clicked
                    button.is_clicked(mouse_pos, True)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("esc pressed in slot selector")
            self.close_callback()
    def draw(self):
        # Clear the screen with a transparent color first

        # Now draw the overlay (it should appear transparent)
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))

        # Draw the "go back" message
        go_back_text = "Press ESC to close"
        go_back_text_surface = self.font2.render(go_back_text, True, (255, 255, 255))
        self.screen.blit(go_back_text_surface, (50, 50))

        # Draw the slot buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)
