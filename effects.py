import pygame
import random
from settings import BLACK, YELLOW, RED, WHITE

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame > 6:
                self.kill()
            else:
                self.image.fill(BLACK)
                # 폭발이 커졌다가 사라지는 원형 애니메이션
                radius = self.frame * 5
                if radius > 0:
                    pygame.draw.circle(self.image, (255, 150, 0), (30, 30), radius)
                    pygame.draw.circle(self.image, (255, 255, 100), (30, 30), radius // 2)

class Spark(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(random.choice([YELLOW, RED, WHITE]))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(random.uniform(-4, 4), random.uniform(-4, 4))
        self.alpha = 255

    def update(self, *args):
        self.pos += self.vel
        self.rect.center = self.pos
        self.alpha -= 15
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)