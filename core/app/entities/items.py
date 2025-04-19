import pygame

class Sword:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/graphics/game/items/sword.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.attack_power = 10
        self.cooldown = 500  # Time between attacks in milliseconds
        self.last_attack_time = pygame.time.get_ticks()

    def attack(self, player, enemies):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.cooldown:
            self.last_attack_time = current_time
            # Attack logic - check for collisions with enemies
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):  # If sword hits enemy
                    enemy.take_damage(self.attack_power)
                    print(f"Attacked enemy! {enemy.name} took {self.attack_power} damage.")
    
    def draw(self, screen, camera):
        # Draw sword relative to player position (camera offset applied)
        camera.apply(self)
        screen.blit(self.image, self.rect)
