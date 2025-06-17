import pygame
from sound_manager import SoundManager

sound_manager = SoundManager()

def show(screen):
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 48)
    option_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 28)
    clock = pygame.time.Clock()

    options = ["Retry", "Main Menu", "Exit Game"]
    selected = 0

    while True:
        screen.fill((0, 0, 0))
        
        # Title
        title = font.render("Game Over", True, (255, 0, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 150))

        # Options
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected else (180, 180, 180)
            option_surface = option_font.render(option, True, color)
            screen.blit(option_surface, (
                screen.get_width() // 2 - option_surface.get_width() // 2,
                280 + i * 50
            ))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sound_manager.play_sfx("choose_option")
                    sound_manager.set_volume(0.4)
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    sound_manager.play_sfx("choose_option")
                    sound_manager.set_volume(0.4)
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    sound_manager.play_sfx("confirm_option")
                    if options[selected] == "Retry":
                        return "playing"
                    elif options[selected] == "Main Menu":
                        return "main_menu"
                    elif options[selected] == "Exit Game":
                        return "quit"
