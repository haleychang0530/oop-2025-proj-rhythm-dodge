import pygame, json
import sys
from player import Player
from particle import Particle
from effect import win_ripple_effect
from triangle import Triangle
from timeline import *
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bpm_scale = 1.06667
time_skip = 10

def tutorial_screen(screen):
    pygame.mixer.music.load("assets/music/tutorial.mp3")
    with open("levels/tutorial.json", "r") as f:
        events = json.load(f)
    pygame.mixer.music.play(start=0.6 + time_skip, fade_ms=500)
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 24)
    x, y = 400, 300
    player = Player(400, 300)
    particles = []
    while True:
        x = random.randint(100, 700)
        y = random.randint(100, 500)
        if 300 < x < 500 and 200 < y < 400:
            continue
        break
    triangle = Triangle((x, y), 20)
    screen_rect = screen.get_rect()

    # Triangle 延遲出現用的計時
    triangle = None
    triangle_spawn_time = 30000  # 延遲 1 秒

    spawned = set()
    particles = []
    prev_obs = []
    obstacles = []

    skip_tutorial = font.render("Press ENTER to skip tutorial", True, (200, 200, 200))

    while True:
        clock.tick(60)
        now = pygame.mixer.music.get_pos() * bpm_scale
        screen.fill((30, 30, 30))
        keys = pygame.key.get_pressed()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "main_menu"  # 跳過教學，進入遊戲

        if triangle is None and now >= triangle_spawn_time:
            while True:
                x = random.randint(100, 700)
                y = random.randint(100, 500)
                if 300 < x < 500 and 200 < y < 400:
                    continue
                break
            triangle = Triangle((x, y), 20)
        
        # 更新並繪製 triangle（如果已生成）
        if triangle:
            triangle.update(screen_rect)
            triangle.draw(screen)

        # 撞到三角形就觸發勝利效果
        if triangle and player.rect.colliderect(triangle.get_rect()):
            sound = pygame.mixer.Sound("assets/sound_effect/mus_sfx_eyeflash.wav")
            sound.play()
            win_ripple_effect(screen, triangle.center)
            pygame.time.delay(100)
            return

        # 玩家更新
        player.update(keys)

        # 粒子拖尾
        if player.dashing:
            particles.append(Particle(player.rect.centerx, player.rect.centery, color=(255, 255, 255), size=8, life=25))
        elif player.alive and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            particles.append(Particle(player.rect.centerx, player.rect.centery, color=(0, 200, 255), size=6, life=20))

        # 更新障礙物
        prev_obs, xx = update_obstacles(screen, screen_rect, particles, events, player, obstacles, spawned, now, prev_obs, bpm_scale, time_skip, 0)
            
        # 繪製畫面
        screen.fill((30, 30, 30))
            
        # 畫邊界/玩家/粒子/障礙
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, 0, 800, 600), 5)

        for o in obstacles:
            o.draw(screen)

        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.life <= 0:
                particles.remove(particle)

        lines = [
            "Arrow Keys: Move",
            "Shift with Arrow Keys: Dash",
        ]

        player.draw(screen)

        for i, text in enumerate(lines):
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, (20, 20 + i * 30))

        screen.blit(skip_tutorial, (WIDTH // 2 - skip_tutorial.get_width() // 2, 500))

        pygame.display.flip()
