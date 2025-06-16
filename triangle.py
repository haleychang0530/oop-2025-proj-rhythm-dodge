import pygame
import math
import random
import time

class Triangle:
    def __init__(self, center, size):
        self.center = list(center)
        self.size = size
        self.sparkle_start_time = time.time()
        self.angle = 0  # 初始旋轉角度
        self.rotation_speed = random.uniform(-2, 2)  # 每幀旋轉角度 (度數)
        self.vx = random.uniform(-1.5, 1.5)  # x方向速度
        self.vy = random.uniform(-1.5, 1.5)  # y方向速度

    def update(self, screen_rect):
        # 更新位置
        self.center[0] += self.vx
        self.center[1] += self.vy

        # 邊界反彈
        if self.center[0] < 50 or self.center[0] > screen_rect.width - 50:
            self.vx *= -1
        if self.center[1] < 50 or self.center[1] > screen_rect.height - 50:
            self.vy *= -1

        # 更新角度（旋轉）
        self.angle += self.rotation_speed
        self.angle %= 360

    def get_points(self):
        x, y = self.center
        size = self.size
        angle_rad = math.radians(self.angle)

        # 三個點的位置（未旋轉時）
        base_points = [
            (0, -size),       # top
            (-size, size),    # bottom-left
            (size, size)      # bottom-right
        ]

        # 套用旋轉矩陣
        rotated_points = []
        for px, py in base_points:
            rx = px * math.cos(angle_rad) - py * math.sin(angle_rad)
            ry = px * math.sin(angle_rad) + py * math.cos(angle_rad)
            rotated_points.append((x + rx, y + ry))

        return rotated_points

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
