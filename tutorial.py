import pygame
import sys
from player import Player
from particle import Particle

def tutorial_screen(screen):
    pygame.display.set_caption("Tutorial")
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 24)

    player = Player(450, 300)
    particles = []

    # Load triangle image
    triangle_img = pygame.image.load("assets/images/boss.png").convert_alpha()
    triangle_img = pygame.transform.scale(triangle_img, (60, 60))
    triangle_rect = triangle_img.get_rect(center=(700, 500))  # Bottom-right corner-ish
    

    while True:
        screen.fill((30, 30, 30))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # === Player Update ===
        player.update(keys)

        # Draw triangle image here
        screen.blit(triangle_img, triangle_rect)    

        # Check if player collides with triangle
        if player.rect.colliderect(triangle_rect):
            pygame.time.delay(500)  
            return  # Exit the tutorial screen

        # === Particle Generation ===
        if player.dashing:
            particles.append(Particle(player.rect.centerx, player.rect.centery, color=(255, 255, 255), size=8, life=25))
        elif player.alive and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            particles.append(Particle(player.rect.centerx, player.rect.centery, color=(0, 200, 255), size=6, life=20))

        # === Particle Update and Draw ===
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.life <= 0:
                particles.remove(particle)

        # === Draw Player ===
        player.draw(screen)

        # === Tutorial instructions ===
        lines = [
            "Arrow Keys: Move",
            "Shift with Arrow Keys: Dash",
            "Try moving around and dashing!"
        ]
        for i, text in enumerate(lines):
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, (20, 20 + i * 30))

        pygame.display.flip()
        clock.tick(60)
