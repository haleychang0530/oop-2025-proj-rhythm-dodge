import pygame
import sys

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
                    sound = pygame.mixer.Sound("assets/sound_effect/snd_block2.wav")
                    sound.set_volume(0.4)
                    sound.play()
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    sound = pygame.mixer.Sound("assets/sound_effect/snd_block2.wav")
                    sound.set_volume(0.4)
                    sound.play()
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    sound = pygame.mixer.Sound("assets/sound_effect/snd_select.wav")
                    sound.play()
                    if options[selected] == "Retry":
                        return "playing"
                    elif options[selected] == "Main Menu":
                        return "main_menu"
                    elif options[selected] == "Exit Game":
                        return "quit"
