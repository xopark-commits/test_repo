import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, YELLOW, RED, WHITE

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self, *args):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, targets):
        super().__init__()
        self.image = pygame.Surface((12, 24))
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, (192, 192, 192), [3, 8, 6, 12])
        pygame.draw.polygon(self.image, RED, [[6, 0], [2, 8], [10, 8]])
        pygame.draw.polygon(self.image, WHITE, [[3, 16], [0, 24], [3, 24]])
        pygame.draw.polygon(self.image, WHITE, [[9, 16], [12, 24], [9, 24]])
        
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(x, y)
        self.rect.center = self.pos
        self.vel = pygame.Vector2(0, -4)
        self.targets = targets
        self.max_speed = 5
        self.max_steering = 0.2

    def update(self, *args):
        target = None
        min_dist = 1000
        for enemy in self.targets:
            dist = self.pos.distance_to(enemy.rect.center)
            if dist < min_dist:
                min_dist = dist
                target = enemy

        if target:
            desired = (pygame.Vector2(target.rect.center) - self.pos).normalize() * self.max_speed
            steering = desired - self.vel
            if steering.length() > self.max_steering:
                steering.scale_to_length(self.max_steering)
            self.vel += steering

        self.pos += self.vel
        self.rect.center = self.pos

        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or \
           self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()