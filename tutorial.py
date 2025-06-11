import pygame
import sys
from player import Player
from particle import Particle
import math
import time

def tutorial_screen(screen):
    pygame.display.set_caption("Tutorial")
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 24)

    player = Player(450, 300)
    particles = []

    # Triangle properties
    triangle_center = (700, 500)
    triangle_size = 40
    sparkle_start_time = time.time()

    def get_triangle_points(center, size):
        x, y = center
        return [
            (x, y - size),
            (x - size, y + size),
            (x + size, y + size)
        ]

    def get_triangle_rect(points):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

    while True:
        screen.fill((30, 30, 30))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # === Player Update ===
        player.update(keys)

        # Sparkling effect (brightness pulsing)
        sparkle_phase = math.sin((time.time() - sparkle_start_time) * 5)  # speed = 5
        brightness = int(128 + 127 * sparkle_phase)
        sparkle_color = (brightness, brightness, brightness)

        # Triangle drawing
        triangle_points = get_triangle_points(triangle_center, triangle_size)
        pygame.draw.polygon(screen, sparkle_color, triangle_points)
        triangle_rect = get_triangle_rect(triangle_points)

        # Collision check with triangle's bounding box
        if player.rect.colliderect(triangle_rect):
            pygame.time.delay(500)
            return  # Exit tutorial and go to next game state

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
