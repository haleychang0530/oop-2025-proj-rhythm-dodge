import pygame
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
SPRINKLE_COLORS = [(255, 192, 203), (255, 255, 0), (0, 255, 255), (255, 105, 180), (144, 238, 144)]

# Sprinkle class
class Sprinkle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, -10)
        self.radius = random.randint(2, 5)
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

# Sprinkle list
sprinkles = []

# Main loop
while True:
    screen.fill((30, 30, 30))  # Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Spawn sprinkles
    if random.random() < 0.2:  # Tune the rate
        sprinkles.append(Sprinkle())

    # Update and draw sprinkles
    for sprinkle in sprinkles[:]:
        sprinkle.update()
        sprinkle.draw(screen)
        if sprinkle.lifetime <= 0 or sprinkle.y > HEIGHT:
            sprinkles.remove(sprinkle)

    pygame.display.flip()
    clock.tick(60)
