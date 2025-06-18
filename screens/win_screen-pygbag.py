import pygame
import random
import sys
import time
from triangle import Triangle
from player import Player
from particle import Particle
from effect import win_ripple_effect
from sound_manager import SoundManager
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()
sound_manager = SoundManager()

# === Fonts and Colors ===
font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 64)
WHITE = (255, 255, 255)
BG_COLOR = (10, 10, 30)

# === 資料結構 ===
class Note:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(1.5, 4.5)
        self.size = random.randint(18, 36)
        self.char = random.choice(["|", "."])
        self.color = random.choice([
            (255, 255, 255)
        ])
        self.font = pygame.font.SysFont("Arial", self.size, bold=True)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.__init__()

    def draw(self, surface):
        label = self.font.render(self.char, True, self.color)
        surface.blit(label, (self.x, self.y))

# === 初始化音符 ===
notes = [Note() for _ in range(50)]

# === 音效（可選）===
# pygame.mixer.init()
# pygame.mixer.Sound("assets/sfx/victory.ogg").play()

def victory_screen(screen):
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.mixer.music.stop()

    #start_time = time.time()
    clock = pygame.time.Clock()
    #font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 64)
    sub_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 24)
    WHITE = (255, 255, 255)
    BG_COLOR = (10, 10, 30)
    x, y = 400, 300
    while True:
        x = random.randint(100, 700)
        y = random.randint(100, 500)
        if 300 < x < 500 and 200 < y < 400:
            continue
        break
    notes = [Note() for _ in range(60)]
    player = Player(400, 300)
    triangle = Triangle(center=(x, y), size=20)
    particles = []

    reached = False
    show_victory = False
    ripple_triggered = False
    ripple_time = 0

    while True:
        dt = clock.tick(60)
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        # background notes
        if show_victory:
            for note in notes:
                note.update()
                note.draw(screen)

        if not reached:
            triangle.update(screen.get_rect()) 
            triangle.draw(screen)

            # particles
            if player.dashing:
                particles.append(Particle(player.rect.centerx, player.rect.centery, color=(255, 255, 255), size=8, life=25))
            elif player.alive and any(keys):
                particles.append(Particle(player.rect.centerx, player.rect.centery, color=(0, 200, 255), size=6, life=20))

            for p in particles[:]:
                p.update()
                p.draw(screen)
                if p.life <= 0:
                    particles.remove(p)

            # check collision
            if player.rect.colliderect(triangle.get_rect()):
                sound = sound_manager.sfx.get("triangle")
                sound.play()
                reached = True
                ripple_triggered = True
                ripple_time = time.time()
                win_ripple_effect(screen, triangle.center)

            player.draw(screen)

        elif ripple_triggered:
            if time.time() - ripple_time > 0.6:
                show_victory = True
                ripple_triggered = False

        elif show_victory:
            # animated text
            scale = 1 + 0.05 * math.sin(pygame.time.get_ticks() / 200)
            font_scaled = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", int(64 * scale))
            text_surf = font_scaled.render("VICTORY!", True, WHITE)
            screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 2 - 60))

            # return hint
            tip = sub_font.render("Press any key to return", True, (180, 180, 180))
            screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, HEIGHT - 50))

            if any(keys):
                return

        pygame.display.flip()

