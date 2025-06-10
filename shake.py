import pygame
import random


import pygame
import random

def shake_surface(screen,surface, shake_duration=15, shake_magnitude=10):
    """
    Returns the (shaken) position and updated shake duration.

    Args:
        surface: The Pygame surface to draw.
        position: Tuple (x, y) where the surface should be drawn.
        shake_duration: Remaining number of frames to shake.
        shake_magnitude: Maximum pixel offset in any direction.

    Returns:
        shaken_position: (x + offset, y + offset)
        new_duration: Updated duration (counted down by 1 if > 0)
    """
    if shake_duration > 0:
        offset_x = random.randint(-shake_magnitude, shake_magnitude)
        offset_y = random.randint(-shake_magnitude, shake_magnitude)
        new_duration = shake_duration - 1
    else:
        offset_x = 0
        offset_y = 0
        new_duration = 0

    surface.draw(screen)
    # self.rect = pygame.Rect(x, y, w, h)
    shaken_position = (surface.x + offset_x, surface.y + offset_y)
    (surface.x,surface.y) = shaken_position
    surface.draw(screen)

    #return new_duration
