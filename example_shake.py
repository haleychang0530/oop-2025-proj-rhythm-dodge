import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Dummy object to visualize shake
object_surface = pygame.Surface((100, 100))
object_surface.fill((255, 0, 0))

# Shake parameters
shake_duration = 0      # Remaining frames to shake
shake_magnitude = 5     # Max pixels to shake

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_SPACE:
            shake_duration = 15  # Start shake for 15 frames

    # Apply shake offset if shaking
    if shake_duration > 0:
        offset_x = random.randint(-shake_magnitude, shake_magnitude)
        offset_y = random.randint(-shake_magnitude, shake_magnitude)
        shake_duration -= 1
    else:
        offset_x = 0
        offset_y = 0

    screen.fill((30, 30, 30))
    screen.blit(object_surface, (270 + offset_x, 190 + offset_y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
