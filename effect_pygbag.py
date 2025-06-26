import pygame
import math
import random

def hurt(o):
    sound = pygame.mixer.Sound("assets/sound_effect/snd_break1.wav")
    """Play audio and visual effect when the player gets hurt."""
    damage = 0
    ob = o.__class__.__name__
    if ob=="FollowObstacle" or ob=="FollowCircleObstacle" or ob=="FollowGearObstacle":
        #sound = pygame.mixer.Sound("assets/sound_effect/snd_arrow.ogg")
        #sound.play()
        damage = 1

    elif ob=="SinCircleObstacle" or ob=="SinObstacle" or ob=="SinGearObstacle" or ob=="RingObstacle":
        #sound = pygame.mixer.Sound("assets/sound_effect/old/ding.ogg")
        #sound.play()
        damage = 2

    elif ob=="LaserCircleObstacle" or ob=="LaserObstacle":
        damage = 0.2
        sound.set_volume(0.5)

    elif ob=="CannonObstacle":
        sound.set_volume(0.4)
        damage = 5
        #sound = pygame.mixer.Sound("assets/sound_effect/snd_buyitem.ogg")
        #sound.play()'''

    elif ob=="CircleObstacle" or ob=="Obstacle" or ob=="GearObstacle":
        damage = 2

    else:
        sound.set_volume(0.1)
    sound.play()
    
    return damage
     

def lazer():
    sound = pygame.mixer.Sound("assets/sound_effect/mus_sfx_rainbowbeam_1.wav")
    sound.set_volume(0.35)
    sound.play(maxtime=1000)


    
def win_ripple_effect(screen, center):
    ripple_radius = 0
    ripple_max_radius = 1000
    clock = pygame.time.Clock()

    white_overlay = pygame.Surface(screen.get_size())
    white_overlay = white_overlay.convert()
    white_overlay.fill((255, 255, 255))

    fade_alpha = 0

    while ripple_radius < ripple_max_radius or fade_alpha < 255:
        screen.fill((30, 30, 30))  # Optional: base color

        # Draw ripple
        if ripple_radius < ripple_max_radius:
            pygame.draw.circle(screen, (255, 255, 255), center, ripple_radius, width=4)
            ripple_radius += 20  # Expand speed

        # Start fade after ripple gets big enough
        if ripple_radius > 300 and fade_alpha < 255:
            fade_alpha = min(255, fade_alpha + 8)
            white_overlay.set_alpha(fade_alpha)
            screen.blit(white_overlay, (0, 0))

        pygame.display.flip()
        clock.tick(60)