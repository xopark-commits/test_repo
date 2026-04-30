import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, RED, WHITE
from weapons import Bullet, Missile

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.set_colorkey(BLACK)
        pygame.draw.polygon(self.image, (130, 130, 130), [[20, 10], [0, 35], [20, 30]])
        pygame.draw.polygon(self.image, (130, 130, 130), [[20, 10], [40, 35], [20, 30]])
        pygame.draw.rect(self.image, (200, 200, 200), [15, 5, 10, 30])
        pygame.draw.polygon(self.image, (200, 200, 200), [[15, 5], [25, 5], [20, 0]])
        pygame.draw.ellipse(self.image, (0, 200, 255), [17, 12, 6, 10])
        pygame.draw.rect(self.image, (255, 100, 0), [18, 35, 4, 5])

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.hp = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.missile_delay = 3000
        self.last_missile = pygame.time.get_ticks()

    def update(self, all_sprites, bullets, enemies):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        
        # 자동으로 총알 발사
        self.shoot(all_sprites, bullets)

        now = pygame.time.get_ticks()
        if now - self.last_missile > self.missile_delay:
            self.last_missile = now
            self.launch_missile(all_sprites, bullets, enemies)

    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def launch_missile(self, all_sprites, bullets, enemies):
        missile_left = Missile(self.rect.left, self.rect.top, enemies)
        missile_right = Missile(self.rect.right, self.rect.top, enemies)
        all_sprites.add(missile_left, missile_right)
        bullets.add(missile_left, missile_right)