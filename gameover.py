import pygame
import sys

def show(screen):
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 48)
    small_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 24)
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        title = font.render("Game Over", True, (255, 0, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 150))

        retry = small_font.render("Press R to Retry", True, (255, 255, 255))
        menu = small_font.render("Press M for Main Menu", True, (255, 255, 255))
        quit_msg = small_font.render("Press Q to Quit", True, (255, 255, 255))

        screen.blit(retry, (screen.get_width()//2 - retry.get_width()//2, 300))
        screen.blit(menu, (screen.get_width()//2 - menu.get_width()//2, 340))
        screen.blit(quit_msg, (screen.get_width()//2 - quit_msg.get_width()//2, 380))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "playing"
                if event.key == pygame.K_m:
                    return "main_menu"
                if event.key == pygame.K_q:
                    return "quit"
