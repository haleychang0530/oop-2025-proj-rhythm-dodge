import pygame, json
from player import Player
from obstacle import *
from particle import Particle
import random
import ui
from start import show_logo_screen
from tutorial import tutorial_screen
from main_menu import main_menu
import timeline
import sys


game_state = "playing"  # or "gameover"

# 初始化 Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JSAB Clone")
clock = pygame.time.Clock()

#start screen
show_logo_screen(screen)
print("Logo screen done")  # <- debugging line

# tutorial screen
tutorial_screen(screen)
print("Tutorial done")

# main menu
level = main_menu(screen)
if not level:
    pygame.quit()
    sys.exit()

if level == 1:
    with open("levels/level1.json", "r") as f:
        events = json.load(f)
elif level == 2:
    with open("levels/level2.json", "r") as f:
        events = json.load(f)


# game start
player = Player(100, 250)
obstacles = []

screen_rect = screen.get_rect()

# 音樂與事件載入
pygame.mixer.music.load("assets/music/bgm.mp3")
pygame.mixer.music.play(start=94.94)
pygame.mixer.music.set_volume(0.3)

with open("levels/level1.json", "r") as f:
    events = json.load(f)

spawned = set()

# 初始化
particles = []
sprinkles=[]
prev_obs = None

running = True
while running:
    dt = clock.tick(60)
    time_now = pygame.mixer.music.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 玩家控制
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Dash 時產生更大的粒子
    if player.dashing:
        particles.append(Particle(player.rect.centerx, player.rect.centery, color=(255, 255, 255), size=8, life=25))
    elif player.alive and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
        # 每幀生成粒子拖尾
        particles.append(Particle(player.rect.centerx, player.rect.centery, color=(0, 200, 255), size=6, life=20))
    
    """把[障礙物生成]之功能搬到timeline.py"""
    prev_obs = timeline.update_obstacles(screen,screen_rect,particles,events,player,obstacles, spawned,time_now,prev_obs)

    # 繪製畫面
    screen.fill((30, 30, 30))
    ui.hud(screen,player.blood)

    # 畫邊界/玩家/粒子/障礙
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, 0, 800, 600), 5)

    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)

    player.draw(screen)

    for p in particles:
        p.draw(screen)

    for o in obstacles:
        o.draw(screen)
    pygame.display.flip()

pygame.quit()