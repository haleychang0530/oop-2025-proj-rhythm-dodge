import pygame, json, sys, random
from player import Player
from obstacle_pygbag import *
from particle import Particle
import ui
from screens.start import start
from screens.tutorial_pygbag import tutorial_screen
from main_menu_pygbag import main_menu
from screens.win_screen import victory_screen
from screens.pause import show_pause_menu
from screens import gameover
from timeline_pygbag import update_obstacles
from sound_manager_pygbag import SoundManager

# 平台偵測（pygbag 專用）
IS_WEB = sys.platform == "emscripten"

# 初始化 Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Dodge")
clock = pygame.time.Clock()

# 全域變數
sound_manager = SoundManager()
game_state = "start"
level = 1
events = []
time_skip = 0
bpm_scale1 = 1.4583
bpm_scale2 = 0.9166
duration = 0
music_was_paused = False
level_initialized = False

# 遊戲主迴圈
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
        # 載入關卡音樂與事件
        if level == 1:
            sound_manager.play_music("assets/music/level1.ogg")
            with open("levels/level1.json", "r") as f:
                events = json.load(f)
        elif level == 2:
            sound_manager.play_music("assets/music/level2.ogg")
            with open("levels/level2.json", "r") as f:
                events = json.load(f)
        pygame.time.delay(500)
        game_state = "playing"

    elif game_state == "playing":
        if not level_initialized:
            player = Player(100, 250)
            obstacles = []
            screen_rect = screen.get_rect()
            if level == 1:
                sound_manager.play_music("assets/music/level1.ogg", start_time=40.94 + time_skip, fade_ms=1000, loop=0)
                bpm_scale = bpm_scale1
                sound_manager.set_volume(0.45)
            elif level == 2:
                sound_manager.play_music("assets/music/level2.ogg", start_time=15.45 + time_skip, fade_ms=1000, loop=0)
                bpm_scale = bpm_scale2
                sound_manager.set_volume(0.4)
            spawned = set()
            particles = []
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

            keys = pygame.key.get_pressed()
            player.update(keys)

            if player.dashing:
                particles.append(Particle(player.rect.centerx, player.rect.centery, color=(255, 255, 255), size=8, life=25))
            elif player.alive and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                particles.append(Particle(player.rect.centerx, player.rect.centery, color=(0, 200, 255), size=6, life=20))

            prev_obs = update_obstacles(screen, screen_rect, particles, events, player, obstacles, spawned, time_now, prev_obs, bpm_scale, time_skip)

            screen.fill((10, 10, 30))
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, 0, 800, 600), 5)
            for o in obstacles:
                o.draw(screen)
            for p in particles[:]:
                p.update()
                if p.life <= 0:
                    particles.remove(p)
            for p in particles:
                p.draw(screen)
            player.draw(screen)

            if not player.alive:
                if inclock < 1:
                    pygame.mixer.music.stop()
                    level_initialized = False
                    game_state = "game_over"
                    sound_manager.play_sfx("dead")
                    sound_manager.set_volume(0.3)
                    inclock += 1
                else:
                    inclock += 1
                if inclock > 19:
                    pygame.time.delay(500)
                    break

            if not sound_manager.is_music_playing() and player.alive and not music_was_paused:
                level_initialized = False
                game_state = "victory"
                break

            ui.hud(screen, player.blood)
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
        game_state = "main_menu"

    elif game_state == "game_over":
        game_state = gameover.show(screen)
        if game_state == "quit":
            pygame.quit()
            sys.exit()