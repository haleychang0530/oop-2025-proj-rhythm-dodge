import pygame, json
from player import Player
from obstacle import *
from particle import Particle
import random
import ui
import effect
from start import show_logo_screen
from tutorial import tutorial_screen

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

time_skip = 0  # 用於時間跳過 for testing

# 音樂與事件載入
pygame.mixer.music.load("assets/music/level2.mp3")
pygame.mixer.music.play(start=41.95 + time_skip) #94.94    # 1:30~2:30 for level 2 
pygame.mixer.music.set_volume(0.3)

with open("levels/level2.json", "r") as f:
    events = json.load(f)

spawned = set()

# 初始化
particles = []
sprinkles=[]

# prev_obstacles
prev_obs = None

bpm_scale1 = 0.975  # 時間縮放因子 for bpm 234
bpm_scale2 = 0.9166 # 時間縮放因子 for bpm 110

running = True
while running:
    dt = clock.tick(60)
    time_now = pygame.mixer.music.get_pos() * bpm_scale2  # 獲取當前時間，並縮放到 bpm 110 的時間尺度

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
        if evt["time"] + 50 > time_now + time_skip * bpm_scale2 * 1000 >= evt["time"] and i not in spawned:
            if evt.get("type") == "sin":
                obs = SinObstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"], amplitude=evt.get("amplitude", 50), frequency=evt.get("frequency", 0.01))
            elif evt.get("type") == "follow":
                obs = FollowObstacle(evt["x"], evt["y"], evt["w"], evt["h"],player , speed=evt.get("speed", 15))
            elif evt.get("type") == "laser":
                obs = LaserObstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"], charge_time=evt.get("charge", 1000)/ bpm_scale2) 
            
            # === 圓形類型 ===
            elif evt.get("type") == "circle":
                obs = CircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"]
                )

            elif evt.get("type") == "circle_sin":
                obs = SinCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    amplitude=evt.get("amplitude", 50),
                    frequency=evt.get("frequency", 0.01)
                )

            elif evt.get("type") == "circle_follow":
                obs = FollowCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    player, speed=evt.get("speed", 15)
                )

            elif evt.get("type") == "circle_laser":
                obs = LaserCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    charge_time=evt.get("charge", 1000) / bpm_scale2
                )
            elif evt.get("type") == "gear":
                obs = GearObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
            )
            elif evt.get("type") == "gear_follow":
                obs = FollowGearObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    player, speed=evt.get("speed", 15),
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
                )
            elif evt.get("type") == "gear_sin":
                obs = SinGearObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    amplitude=evt.get("amplitude", 50),
                    frequency=evt.get("frequency", 0.01),
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
                )
            elif evt.get("type") == "cannon":
                obs = CannonObstacle(
                    evt["x"], evt["y"], evt["w"], evt["h"],
                    evt["vx"], evt["vy"], evt.get("amplitude", 300)
                    ,evt.get("wave", 2000), evt.get("bar", 51)
                    
                )
            else:
                obs = Obstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"])
            obstacles.append(obs)
            spawned.add(i)
    
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
                for _ in range(30):
                    particles.append(Particle(player.rect.centerx, player.rect.centery))
            
    if all_pass:
        prev_obs = None

    # 繪製畫面
    screen.fill((30, 30, 30))
    ui.hud(screen,player.blood)
   
    
    #sprinkle.sprinkle(screen,sprinkles,WIDTH, HEIGHT)

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