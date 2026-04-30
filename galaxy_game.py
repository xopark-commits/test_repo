import pygame
import sys
import random
from settings import *
from player import Player
from enemy import Enemy
from background import Star, draw_hp_bar
from effects import Explosion, Spark

# 1. 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaga Style Game")
clock = pygame.time.Clock()

# 게임 화면용 서피스 (흔들림 효과 구현용)
game_display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
shake_time = 0

def show_gameover_screen():
    """게임 오버 화면을 표시하고 재시작 여부를 반환함"""
    start_ticks = pygame.time.get_ticks()
    big_font = pygame.font.SysFont("malgungothic", 60, True)
    mid_font = pygame.font.SysFont("malgungothic", 30)
    
    while True:
        # 카운트다운 계산 (10초)
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining = 10 - seconds
        
        if remaining <= 0:
            return False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                if event.key == pygame.K_n:
                    return False
        
        # 화면 그리기
        game_display.fill(BLACK)
        
        title_text = big_font.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        game_display.blit(title_text, title_rect)
        
        retry_text = mid_font.render("Continue? (Y / N)", True, WHITE)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        game_display.blit(retry_text, retry_rect)
        
        count_text = big_font.render(str(remaining), True, YELLOW)
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        game_display.blit(count_text, count_rect)
        
        # 흔들림 효과 없이 메인 화면에 출력
        screen.fill(BLACK)
        screen.blit(game_display, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

# 3. 스프라이트 그룹 생성 및 인스턴스화
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
stars = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(25): # 25개의 별 생성 (숫자를 반으로 줄임)
    star = Star()
    stars.add(star)

for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

score = 0
font = pygame.font.SysFont("malgungothic", 30)

# 4. 게임 루프
running = True
while running:
    clock.tick(FPS)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 업데이트
    stars.update()
    all_sprites.update(all_sprites, bullets, enemies)

    # 충돌 체크 (총알과 적)
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)

    # 충돌 체크 (플레이어와 적)
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.hp -= 10
        shake_time = 15 # 흔들림 지속 시간
        
        # 플레이어 위치에서 불꽃(Spark) 생성
        for _ in range(15):
            spark = Spark(player.rect.center)
            all_sprites.add(spark)
            
        # 적이 터지는 폭발 효과
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)
        
        # 충돌한 적 대신 새로운 적 생성
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)
        if player.hp <= 0:
            if show_gameover_screen():
                # 게임 초기화 (재시작)
                score = 0
                player = Player()
                all_sprites.empty()
                enemies.empty()
                bullets.empty()
                stars.empty()
                
                all_sprites.add(player)
                for i in range(25):
                    star = Star()
                    stars.add(star)
                for i in range(8):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)
                shake_time = 0
            else:
                running = False # 게임 종료

    # 그리기
    game_display.fill(BLACK)
    stars.draw(game_display) # 별을 먼저 그려서 배경으로 설정
    all_sprites.draw(game_display)
    
    # 점수 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    game_display.blit(score_text, (10, 10))
    
    # 체력바 표시
    draw_hp_bar(game_display, SCREEN_WIDTH - 120, 20, player.hp)

    # 화면 흔들림 계산
    render_offset = [0, 0]
    if shake_time > 0:
        render_offset[0] = random.randint(-4, 4)
        render_offset[1] = random.randint(-4, 4)
        shake_time -= 1

    screen.fill(BLACK)
    screen.blit(game_display, render_offset)

    pygame.display.flip()

# 종료 처리
pygame.quit()
sys.exit()
