import pygame, json, sys, random
from player import Player
from obstacle import *
from particle import Particle
import ui
from start import start
from tutorial import tutorial_screen
from main_menu import main_menu
from timeline import update_obstacles  
from worklog.lightning import Lightning
# 初始化 Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Dodge")
clock = pygame.time.Clock()

game_state = "start"
level = 1
events = []
time_skip = 0  # 用於時間跳過 for testing
bpm_scale_sp = 0.975  # 時間縮放因子 for bpm 234
bpm_scale1 = 1.4583  # 時間縮放因子 for bpm 175
bpm_scale2 = 0.9166 # 時間縮放因子 for bpm 110

while True:
    if game_state == "start":
        start(screen)
        game_state = "tutorial"
    
    elif game_state == "tutorial":
        tutorial_screen(screen)
        game_state = "main_menu"

    elif game_state == "main_menu":
        level = main_menu(screen)
        if not level:
            pygame.quit()
            sys.exit()
        if level == 1:
            pygame.mixer.music.load("assets/music/level1.mp3")
            with open("levels/level1.json", "r") as f:
                events = json.load(f)
        elif level == 2:
            pygame.mixer.music.load("assets/music/level2.mp3")
            with open("levels/level2.json", "r") as f:
                events = json.load(f)
        pygame.time.delay(500)
        game_state = "playing"

    elif game_state == "playing":
        # game start
        player = Player(100, 250)
        obstacles = []
        screen_rect = screen.get_rect()
        # 音樂與事件載入
        
        if level == 1:
            pygame.mixer.music.play(start=0) #未確定
            bpm_scale = bpm_scale1
        elif level == 2:
            pygame.mixer.music.play(start=15.45 + time_skip)
            bpm_scale = bpm_scale2
        
        pygame.mixer.music.set_volume(0.5)

        #with open("levels/level1.json", "r") as f:
            #events = json.load(f)

        spawned = set()

        # 初始化
        particles = []
        sprinkles=[]
        prev_obs = []
        running = True

        while running:
            dt = clock.tick(60)
            time_now = pygame.mixer.music.get_pos() * bpm_scale

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
            '''if level == 1:
                prev_obs = level1.update_obstacles(screen,screen_rect,particles,events,player,obstacles, spawned,time_now,prev_obs)
            elif level == 2:
                prev_obs = update_obstacles(screen, screen_rect, particles, events, player, obstacles, spawned, time_now, prev_obs,bpm_scale2,time_skip)
            '''
            '''再次扳回timeline.py'''
            # 更新障礙物
            prev_obs = update_obstacles(screen, screen_rect, particles, events, player, obstacles, spawned, time_now, prev_obs, bpm_scale, time_skip)
            # 繪製畫面
            screen.fill((30, 30, 30))
            

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


            # 玩家死亡判定
            if not player.alive:
                print("玩家死亡，切換到 game_over 畫面")  # <--- 新增
                pygame.mixer.music.stop()
                game_state = "game_over"
                pygame.time.delay(1000)  # 停一秒，讓玩家有時間看到死掉
                break

            ui.hud(screen,player.blood)
            pygame.display.flip()
           

    elif game_state == "game_over":
        # 顯示 Game Over 畫面
        import gameover
        game_state = gameover.show(screen)  # 回傳 "main_menu" 或 "playing" 或 "quit"
        if game_state == "quit":
            pygame.quit()
            sys.exit()
