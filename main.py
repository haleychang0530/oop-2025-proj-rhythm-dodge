import pygame, json
from player import Player
from obstacle import Obstacle , SinObstacle, FollowObstacle, LaserObstacle
from particle import Particle
import random
import ui

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JSAB Clone")
clock = pygame.time.Clock()

player = Player(100, 250)
obstacles = []


# 音樂與事件載入
pygame.mixer.music.load("assets/music/bgm.mp3")
pygame.mixer.music.play(start=95)
with open("levels/level1.json", "r") as f:
    events = json.load(f)

spawned = set()

# 初始化粒子系統
particles = []

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
    

    # 障礙物生成（依時間）
    for i, evt in enumerate(events):
        if time_now >= evt["time"]*1.02564 and i not in spawned: # 1.02564 是時間縮放因子 for bpm 234
            if evt.get("type") == "sin":
                obs = SinObstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"], amplitude=evt.get("amplitude", 50), frequency=evt.get("frequency", 0.01))
            elif evt.get("type") == "follow":
                obs = FollowObstacle(evt["x"], evt["y"], evt["w"], evt["h"],player , speed=evt.get("speed", 15))
            elif evt.get("type") == "laser":
                obs = LaserObstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"], charge_time=evt.get("charge", 1000)*1.02564)
            else:
                obs = Obstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"])
            obstacles.append(obs)
            spawned.add(i)

    # 更新障礙物
    for o in obstacles:
        o.update()
        if isinstance(o, LaserObstacle) and o.expired:
            obstacles.remove(o)
        if player.rect.colliderect(o.rect) and player.alive and not player.dashing:
            if isinstance(o, LaserObstacle) and not o.activated:
                continue  # 預熱中的雷射不造成傷害

             # 0607 小改:血條
            if prev_obs != o:
                player.blood = player.blood - 1
                prev_obs = o
            

            # player.alive = False
            for _ in range(30):
                particles.append(Particle(player.rect.centerx, player.rect.centery))

    # 繪製畫面
    screen.fill((30, 30, 30))
    ui.hud(screen,player.blood)

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