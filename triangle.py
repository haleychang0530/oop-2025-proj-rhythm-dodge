import pygame
import math
import time

class Triangle:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.sparkle_start_time = time.time()

    def get_points(self):
        x, y = self.center
        size = self.size
        return [
            (x, y - size),         # top
            (x - size, y + size),  # bottom-left
            (x + size, y + size)   # bottom-right
        ]

    def get_rect(self):
        points = self.get_points()
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

    def draw(self, surface, border_width=4):
        # Sparkling effect
        phase = math.sin((time.time() - self.sparkle_start_time) * 5)
        brightness = int(128 + 127 * phase)
        sparkle_color = (brightness, brightness, brightness)

        # Optional: outer glow
        pygame.draw.polygon(surface, (255, 255, 255), self.get_points(), width=border_width + 2)
        # Main triangle
        pygame.draw.polygon(surface, sparkle_color, self.get_points(), width=border_width)
