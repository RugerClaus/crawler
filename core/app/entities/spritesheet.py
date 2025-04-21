import pygame

class SpriteSheet:
    def __init__(self, image_path):
        self.sheet = pygame.image.load(image_path).convert_alpha()
        print(f"Sprite sheet loaded: {self.sheet.get_size()}")  # Expecting 192x192

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        print(f"Extracted sprite size: {sprite.get_size()}")
        
        # Adjust x and y based on grid positions in the spritesheet
        sprite.blit(self.sheet, (0, 0), (x * width, y * height, width, height))  # x * width and y * height
        return sprite

    def get_animation(self, frame_width, frame_height, num_frames, start_x=0, start_y=0, spacing=0):
        frames = []
        for i in range(num_frames):
            x = start_x + (frame_width + spacing) * i
            y = start_y
            frame = self.get_sprite(x, y, frame_width, frame_height)
            frames.append(frame)
        return frames
