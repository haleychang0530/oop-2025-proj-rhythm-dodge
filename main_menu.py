# main_menu.py
import pygame

def main_menu(screen):
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()

    font_title = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 64)
    font_option = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 36)

    options = ["Level 1", "Level 2"]
    selected = 0

    while True:
        screen.fill((10, 10, 30))

        # Title
        title = font_title.render("JSAB Clone", True, (255, 100, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

        # Menu Options
        for i, text in enumerate(options):
            color = (255, 255, 255) if i == selected else (150, 150, 150)
            label = font_option.render(text, True, color)
            screen.blit(label, (screen.get_width() // 2 - label.get_width() // 2, 250 + i * 60))

        pygame.display.flip()
        clock.tick(60)

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected + 1  # return level number
