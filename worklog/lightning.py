import pygame
import random

# === Lightning class ===
class Lightning:
    def __init__(self, start_pos, end_pos, color=(255, 255, 0), thickness=5, segments=10, offset=20):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.thickness = thickness
        self.segments = segments
        self.offset = offset
        self.path = self.generate_path()

    def generate_path(self):
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos

        points = [self.start_pos]
        for i in range(1, self.segments):
            t = i / self.segments
            nx = x1 + t * (x2 - x1)
            ny = y1 + t * (y2 - y1)
            dx = -(y2 - y1)
            dy = (x2 - x1)
            length = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            dx /= length
            dy /= length
            deviation = random.uniform(-self.offset, self.offset)
            nx += dx * deviation
            ny += dy * deviation
            points.append((nx, ny))
        points.append(self.end_pos)
        return points

    def draw(self, surface):
        pygame.draw.lines(surface, self.color, False, self.path, self.thickness)


"""# === Pygame setup ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

# Create initial lightning
start = (WIDTH // 2, HEIGHT // 4)
end = (WIDTH // 2, HEIGHT * 3 // 4)
lightning = Lightning(start, end)

# === Main loop ===
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Optional: regenerate to make it flicker
    lightning.path = lightning.generate_path()

    # === Draw ===
    screen.fill((0, 0, 0))  # black background
    lightning.draw(screen)

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()"""


