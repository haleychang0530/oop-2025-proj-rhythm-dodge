import pygame
import sys
from player import Player
from particle import Particle
from effect import win_ripple_effect
from triangle import Triangle
import random

def tutorial_screen(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 24)

    player = Player(450, 300)
    particles = []

    triangle = Triangle((random.randint(100, 700), random.randint(100, 500)), 20)
    screen_rect = screen.get_rect()

    while True:
        screen.fill((30, 30, 30))

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 更新並繪製單一 triangle
        triangle.update(screen_rect)
        triangle.draw(screen)

        # 撞到三角形就觸發勝利效果
        if player.rect.colliderect(triangle.get_rect()):
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

        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.life <= 0:
                particles.remove(particle)

        player.draw(screen)

        lines = [
            "Arrow Keys: Move",
            "Shift with Arrow Keys: Dash",
        ]
        for i, text in enumerate(lines):
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, (20, 20 + i * 30))

        pygame.display.flip()
        clock.tick(60)
