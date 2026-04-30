import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey(BLACK)

        colors = [(255, 50, 50), (50, 255, 50), (50, 150, 255), (255, 100, 255), (255, 200, 50), (0, 255, 255)]
        color = random.choice(colors)

        shape_type = random.randint(0, 2)
        if shape_type == 0: # 비행기 모양
            pygame.draw.polygon(self.image, color, [[0, 0], [30, 0], [15, 25]])
            pygame.draw.rect(self.image, WHITE, [12, 5, 6, 5]) 
        elif shape_type == 1: # 게 모양
            pygame.draw.rect(self.image, color, [7, 7, 16, 12])
            pygame.draw.line(self.image, color, [7, 7], [0, 0], 3)
            pygame.draw.line(self.image, color, [23, 7], [30, 0], 3)
            pygame.draw.line(self.image, color, [7, 19], [0, 28], 3)
            pygame.draw.line(self.image, color, [23, 19], [30, 28], 3)
        else: # UFO 모양
            pygame.draw.ellipse(self.image, color, [0, 8, 30, 14])
            pygame.draw.ellipse(self.image, WHITE, [10, 4, 10, 8])

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self, *args):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)