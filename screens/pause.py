# pause.py
import pygame
from sound_manager import SoundManager

sound_manager = SoundManager()

def show_pause_menu(screen, clock, WIDTH, HEIGHT):
    pause_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 48)
    option_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 30)

    options = ["Resume", "Retry", "Main Menu"]
    selected = 0
    paused = True

    while paused:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                    sound_manager.play_sfx("choose_option")
                    sound_manager.set_volume(0.4) 
                elif event.key == pygame.K_DOWN:
                    sound_manager.play_sfx("choose_option")
                    sound_manager.set_volume(0.4)                 
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    sound_manager.play_sfx("confirm_option")
                    return options[selected].lower()  # "resume", "retry", "main menu"

        screen.fill((10, 10, 30))
        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 120))

        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected else (180, 180, 180)
            text_surface = option_font.render(option, True, color)
            screen.blit(text_surface, (
                WIDTH // 2 - text_surface.get_width() // 2,
                HEIGHT // 2 - 30 + i * 50 + 70
            ))

        pygame.display.flip()
        clock.tick(30)
