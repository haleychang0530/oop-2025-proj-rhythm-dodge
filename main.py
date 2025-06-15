import pygame, json, sys, random
from player import Player
from obstacle import *
from particle import Particle
import ui
from screens.start import start
from screens.tutorial import tutorial_screen
from screens.main_menu import main_menu
from screens.win_screen import victory_screen
from screens.pause import show_pause_menu
from screens import gameover
from timeline import update_obstacles  

# 初始化 Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Dodge")
clock = pygame.time.Clock()

game_state = "start"
level = 1
events = []
time_skip = 55 # 用於時間跳過 for testing
bpm_scale_sp = 0.975  # 時間縮放因子 for bpm 234
bpm_scale1 = 1.4583  # 時間縮放因子 for bpm 175
bpm_scale2 = 0.9166 # 時間縮放因子 for bpm 110
duration = 0  # 用於光線效果的持續時間
# variables for pause during game
music_was_paused = False
level_initialized = False


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
        if not level_initialized:
            # game start
            player = Player(100, 250)
            obstacles = []
            screen_rect = screen.get_rect()
            music_was_paused = False  

            # 音樂與事件載入
            if level == 1:
                pygame.mixer.music.play(start=40.94 + time_skip, fade_ms=1000)
                bpm_scale = bpm_scale1
                pygame.mixer.music.set_volume(0.45)
            elif level == 2:
                pygame.mixer.music.play(start=15.45 + time_skip, fade_ms=1000)
                bpm_scale = bpm_scale2
                pygame.mixer.music.set_volume(0.4)
            

            #with open("levels/level1.json", "r") as f:
                #events = json.load(f)

            # 初始化
            spawned = set()
            particles = []
            sprinkles=[]
            prev_obs = []
            level_initialized = True
            inclock = 0

        running = True

        while running:
            dt = clock.tick(60)
            time_now = pygame.mixer.music.get_pos() * bpm_scale

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.pause()
                        game_state = "pause"
                        music_was_paused = True
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
            prev_obs, duration = update_obstacles(screen, screen_rect, particles, events, player, obstacles, spawned, time_now, prev_obs, bpm_scale, time_skip, duration)
            
            # 繪製畫面
            screen.fill((30, 30, 30))
            
            # 畫邊界/玩家/粒子/障礙
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, 0, 800, 600), 5)

            for o in obstacles:
                o.draw(screen)  

            for p in particles[:]:
                p.update()
                if p.life <= 0:
                    particles.remove(p)
            if duration > 0:
                effect.draw_radial_beams(screen, player.rect.center,duration)
            player.draw(screen)

            for p in particles:
                p.draw(screen)

            # 玩家死亡判定
            if not player.alive:
                if inclock < 1:
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                    level_initialized = False
                    game_state = "game_over"
                    sound = pygame.mixer.Sound("assets/sound_effect/mus_sfx_a_lithit.wav")
                    sound.set_volume(0.3)
                    sound.play()
                    inclock += 1
                else:
                    inclock += 1
                if inclock > 19:
                    print("玩家死亡，切換到 game_over 畫面")  # <--- 新增
                    pygame.time.delay(500)  # 停一秒，讓玩家有時間看到死掉
                    break

            if not pygame.mixer.music.get_busy() and player.alive and not music_was_paused:
                print("玩家通關成功！")
                level_initialized = False
                game_state = "victory"
                break

            ui.hud(screen,player.blood)
            pygame.display.flip()
    

    elif game_state == "pause":
        result = show_pause_menu(screen, clock, WIDTH, HEIGHT)
        if result == "resume":
            pygame.mixer.music.unpause()
            music_was_paused = False
            game_state = "playing"
        elif result == "retry":
            level_initialized = False
            game_state = "playing"
        elif result == "main menu":
            game_state = "main_menu"
            level_initialized = False

        
    elif game_state == "victory":
        victory_screen(screen)
        game_state = "main_menu"  #  去選單

    elif game_state == "game_over":
        # 顯示 Game Over 畫面
   
        game_state = gameover.show(screen)  # 回傳 "main_menu" 或 "playing" 或 "quit"
        if game_state == "quit":
            pygame.quit()
            sys.exit()
