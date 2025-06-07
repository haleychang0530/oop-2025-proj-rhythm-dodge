import pygame
import math


class Obstacle:
    def __init__(self, x, y, w, h, vx, vy):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 50, 50)
        self.vx = vx
        self.vy = vy

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class SinObstacle(Obstacle):
    def __init__(self, x, y, w, h, vx, vy, amplitude, frequency):
        super().__init__(x, y, w, h, vx, vy)
        self.base_y = self.rect.y
        self.amplitude = amplitude
        self.frequency = frequency
        self.start_time = pygame.time.get_ticks()

    def update(self):
        super().update()
        t = (pygame.time.get_ticks() - self.start_time)
        self.rect.y = self.base_y + self.amplitude * math.sin(t * self.frequency)

class FollowObstacle(Obstacle):
    def __init__(self, x, y, w, h, player, speed):
        # 計算指向玩家的方向向量
        dx = player.rect.centerx - x
        dy = player.rect.centery - y
        length = max(1, math.hypot(dx, dy))

        # 單位方向向量乘以速度
        vx = dx / length * speed
        vy = dy / length * speed

        super().__init__(x, y, w, h, vx, vy)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

class LaserObstacle(Obstacle):
    def __init__(self, x, y, w, h, vx, vy, charge_time, duration=500*1.02564):
        super().__init__(x, y, w, h, vx, vy)
        self.charge_time = charge_time      # 充能時間
        self.duration = duration            # 激活後持續時間（毫秒）
        self.spawn_time = pygame.time.get_ticks()
        self.activated = False
        self.expired = False                # 是否應該被移除

    def update(self):
        now = pygame.time.get_ticks()

        # 判斷是否啟動
        if not self.activated and now - self.spawn_time >= self.charge_time:
            self.activated = True
            self.activate_time = now  # 記錄啟動的時間

        # 若已啟動，判斷是否超時
        if self.activated and now - self.activate_time >= self.duration:
            self.expired = True

        
    
    def draw(self, screen):
        laser_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
    
        if not self.activated:
            color = (200, 50, 50, 100)  # 未啟動：淡藍透明
        else:
            color = (200, 0, 0, 255)      # 啟動：紅色半透明

        pygame.draw.rect(laser_surface, color, (0, 0, self.rect.width, self.rect.height))
        screen.blit(laser_surface, (self.rect.x, self.rect.y))

class CircleObstacle(Obstacle):
    def __init__(self, x, y, radius, vx, vy):
        super().__init__(x, y, radius * 2, radius * 2, vx, vy)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

class FollowCircleObstacle(CircleObstacle):
    def __init__(self, x, y, radius, player, speed):
        dx = player.rect.centerx - x
        dy = player.rect.centery - y
        length = max(1, math.hypot(dx, dy))
        vx = dx / length * speed
        vy = dy / length * speed

        super().__init__(x, y, radius, vx, vy)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

class SinCircleObstacle(CircleObstacle):
    def __init__(self, x, y, radius, vx, vy, amplitude, frequency):
        super().__init__(x, y, radius, vx, vy)
        self.base_y = self.rect.y
        self.amplitude = amplitude
        self.frequency = frequency
        self.start_time = pygame.time.get_ticks()

    def update(self):
        super().update()
        t = pygame.time.get_ticks() - self.start_time
        self.rect.y = self.base_y + self.amplitude * math.sin(t * self.frequency)

class LaserCircleObstacle(CircleObstacle):
    def __init__(self, x, y, radius, vx, vy, charge_time, duration=500*1.02564):
        super().__init__(x, y, radius, vx, vy)
        self.charge_time = charge_time
        self.duration = duration
        self.spawn_time = pygame.time.get_ticks()
        self.activated = False
        self.expired = False

    def update(self):
        now = pygame.time.get_ticks()
        if not self.activated and now - self.spawn_time >= self.charge_time:
            self.activated = True
            self.activate_time = now
        if self.activated and now - self.activate_time >= self.duration:
            self.expired = True

    def draw(self, screen):
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        color = (200, 50, 50, 100) if not self.activated else (255, 0, 0, 255)
        pygame.draw.circle(surface, color, (self.radius, self.radius), self.radius)
        screen.blit(surface, (self.rect.x, self.rect.y))