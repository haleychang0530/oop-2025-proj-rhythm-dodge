import pygame
import sys

def show_tutorial(screen):
    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.SysFont("Arial", 40, bold=True)
    small_font = pygame.font.SysFont("Arial", 25)

    instructions = [
        "Controls:",
        "Arrow Keys - Move",
        "Shift - Dash",
        "Avoid obstacles and survive!",
        "",
        "Press ENTER to start the game"
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Exit tutorial screen

        screen.fill(BLACK)

        for i, line in enumerate(instructions):
            text_surface = font.render(line, True, WHITE) if i == 0 else small_font.render(line, True, WHITE)
            screen.blit(text_surface, (50, 100 + i * 50))

        pygame.display.flip()
        clock.tick(60)
