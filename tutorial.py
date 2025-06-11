import pygame
import sys
from player import Player
from particle import Particle
from effect import win_ripple_effect
from triangle import Triangle
import math
import time


def tutorial_screen(screen):
    pygame.display.set_caption("Tutorial")
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 24)

    player = Player(450, 300)
    particles = []

    triangle = Triangle(center=(700, 500), size=12)

    while True:
        screen.fill((30, 30, 30))
        triangle.draw(screen)

        if player.rect.colliderect(triangle.get_rect()):
            win_ripple_effect(screen, triangle.center)
            pygame.time.delay(500)
            return

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # === Player Update ===
        player.update(keys)

        # === Particle Generation ===
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

        # Instructions
        lines = [
            "Arrow Keys: Move",
            "Shift with Arrow Keys: Dash",
            "Touch the sparkling triangle to finish tutorial!"
        ]
        for i, text in enumerate(lines):
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, (20, 20 + i * 30))

        pygame.display.flip()
        clock.tick(60)
