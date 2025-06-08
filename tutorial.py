# tutorial.py
import pygame
import sys
from player import Player

def tutorial_screen(screen):
    pygame.display.set_caption("Tutorial")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    
    player = Player(100, 100)

    while True:
        screen.fill((30, 30, 30))
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # proceed to next screen

        player.update(keys)
        player.draw(screen)

        # === Tutorial instructions ===
        lines = [
            "Arrow Keys: Move",
            "Shift with Arror Keys: Dash",
            "Try moving around and dashing!",
            "Press ENTER to continue"
        ]
        for i, text in enumerate(lines):
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, (20, 20 + i * 30))

        pygame.display.flip()
        clock.tick(60)
