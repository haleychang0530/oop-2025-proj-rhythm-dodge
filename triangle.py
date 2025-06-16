import pygame
import math
import time
import random

class Triangle:
    def __init__(self, center, size):
        self.center = list(center)  # 需要可修改的座標
        self.size = size
        self.sparkle_start_time = time.time()
        self.angle = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.05, 0.05)

        # 隨機速度向量
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

    def update(self, screen_rect):
        # 移動
        self.center[0] += self.velocity[0]
        self.center[1] += self.velocity[1]

        # 旋轉
        self.angle += self.rotation_speed

        # 碰到邊緣就反彈
        if not screen_rect.contains(self.get_rect()):
            if self.center[0] < screen_rect.left or self.center[0] > screen_rect.right:
                self.velocity[0] *= -1
            if self.center[1] < screen_rect.top or self.center[1] > screen_rect.bottom:
                self.velocity[1] *= -1

    def get_points(self):
        x, y = self.center
        size = self.size
        # 定義等邊三角形的三個頂點
        points = [
            (0, -size),
            (-size, size),
            (size, size)
        ]
        # 套用旋轉矩陣
        rotated = []
        for px, py in points:
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            rotated.append((x + rx, y + ry))
        return rotated

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

        pygame.draw.polygon(surface, (255, 255, 255), self.get_points(), width=border_width + 2)
        pygame.draw.polygon(surface, sparkle_color, self.get_points(), width=border_width)
