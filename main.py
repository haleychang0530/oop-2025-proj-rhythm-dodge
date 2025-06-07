import pygame, json
from player import Player
from obstacle import Obstacle
from particle import Particle


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JSAB Clone")
clock = pygame.time.Clock()

player = Player(100, 250)
obstacles = []

# 音樂與事件載入
pygame.mixer.music.load("assets/bgm.mp3")
pygame.mixer.music.play(start=95)
with open("level.json", "r") as f:
    events = json.load(f)

spawned = set()

# 初始化粒子系統
particles = []

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
            o = Obstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"])
            obstacles.append(o)
            spawned.add(i)

    # 更新障礙物
    for o in obstacles:
        o.update()
        if player.rect.colliderect(o.rect) and player.alive and not player.dashing:
            player.alive = False
            # 粒子爆炸
            for _ in range(30):
                particles.append(Particle(player.rect.centerx, player.rect.centery))

    # 繪製畫面
    screen.fill((30, 30, 30))

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