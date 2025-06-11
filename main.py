import pygame, json
from player import Player
from obstacle import *
from particle import Particle
import random
import ui
import effect
from start import show_logo_screen
from tutorial import tutorial_screen
import timeline

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

# prev_obstacles
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
    
    """把[障礙物生成（依時間）]之功能搬到timeline.py"""
    obstacles, spawned = timeline.update_obstacles(events,player,obstacles, spawned,time_now)

    # 更新障礙物
    all_pass = True
    for o in obstacles:
        if isinstance(o, CannonObstacle):
            o.update(screen_rect, player)
        else:
            o.update()    
        if ( isinstance(o, LaserObstacle) or isinstance(o, LaserCircleObstacle)) and o.expired:
            obstacles.remove(o)

        if not screen.get_rect().colliderect(o.rect):
            obstacles.remove(o)

        # 檢查玩家與障礙物碰撞
        if player.alive and not player.dashing:
            if ( isinstance(o,CircleObstacle) or isinstance(o, SinCircleObstacle) or isinstance(o, FollowCircleObstacle) or isinstance(o, LaserCircleObstacle) 
                or isinstance(o, GearObstacle) or isinstance(o, SinGearObstacle) or isinstance(o, FollowGearObstacle) ):
                # 圓形障礙物的碰撞檢查
                if o.collide(player):
                    if isinstance(o, LaserCircleObstacle) and not o.activated:
                        continue  # 預熱中的雷射不造成傷害
                    if prev_obs != o and player.blood > 0:
                        all_pass=False
                        player.blood = player.blood - 1
                        prev_obs = o
                        effect.hurt(o)
                        o.shake()
                    for _ in range(30):
                        particles.append(Particle(player.rect.centerx, player.rect.centery))
            elif player.rect.colliderect(o.rect):
                if ( isinstance(o, LaserObstacle) and not o.activated or (isinstance(o, CannonObstacle) and o.expired)):
                    continue  # 預熱中的雷射不造成傷害
                if prev_obs != o and player.blood > 0:
                    all_pass=False
                    player.blood = player.blood - 1
                    prev_obs = o
                    effect.hurt(o)
                    o.shake()
                for _ in range(30):
                    particles.append(Particle(player.rect.centerx, player.rect.centery))
            
    if all_pass:
        prev_obs = None

    # 繪製畫面
    screen.fill((30, 30, 30))
    ui.hud(screen,player.blood)

    # 畫邊界
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
# 退出遊戲