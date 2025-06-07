import pygame
import sprinkle

def hurt(screen,player):
    """Play audio and visual effect when the player gets hurt."""
    sound = pygame.mixer.Sound("assets/music/biu.wav")
    sound.play()
    
    