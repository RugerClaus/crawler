import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, screen, solid=True, health=1):
        super().__init__()
        self.screen = screen
        self.solid = solid
        self.health = health
        self.image = None
        self.rect = None
        self.animations = {}
        self.animation = None

    def set_animation(self, name, animation_obj):
        self.animations[name] = animation_obj

    def play_animation(self, name):
        if self.animation != self.animations.get(name):
            self.animation = self.animations.get(name)
            if self.animation:
                self.animation.reset()
                self.image = self.animation.get_current_frame()  # <-- set image immediately

    def update_animation(self):
        if self.animation:
            self.animation.update()
            self.image = self.animation.get_current_frame()

    def draw(self, camera):
        if self.image and self.rect:
            render_rect = camera.apply(self.rect)
            self.screen.blit(self.image, render_rect)
