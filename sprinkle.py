import pygame
import random
import sys

# Colors
SPRINKLE_COLORS = [(255, 192, 203), (255, 255, 0), (0, 255, 255), (255, 105, 180), (144, 238, 144)]

# Sprinkle class
class Sprinkle:
    def __init__(self):
        self.x = random.randint(0, 1400)
        self.y = random.randint(0, 700)
        self.radius = random.randint(10, 30)
        self.color = random.choice(SPRINKLE_COLORS)
        self.speed_y = random.uniform(1, 3)
        self.speed_x = random.uniform(-1, 1)
        self.lifetime = random.randint(60, 120)  # frames

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

def sprinkle(screen,sprinkles,WIDTH, HEIGHT):
    # Spawn sprinkles
    if random.random() < 0.2:  # Tune the rate
        sprinkles.append(Sprinkle())

    # Update and draw sprinkles
    for sprinkle in sprinkles[:]:
        sprinkle.update()
        sprinkle.draw(screen)
        if sprinkle.lifetime <= 0 or sprinkle.y > HEIGHT:
            sprinkles.remove(sprinkle)