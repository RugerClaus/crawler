# camera.py
class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height

    def update(self, target):
        # Target is usually your Player object
        self.offset_x = target.world_x - self.width // 2
        self.offset_y = target.world_y - self.height // 2

        # Optional: Clamp to world bounds
        self.offset_x = max(0, self.offset_x)
        self.offset_y = max(0, self.offset_y)

    def apply(self, rect):
        # Return a rect with camera offset applied
        return rect.move(-self.offset_x, -self.offset_y)