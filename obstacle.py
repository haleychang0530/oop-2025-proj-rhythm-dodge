import pygame
import math
import effect

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

class GearObstacle():
    def __init__(self, x, y, radius, vx, vy, teeth=12, color=(255, 0, 0), rotation_speed=2):
        self.x = x + radius
        self.y = y + radius
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.teeth = teeth
        self.color = color
        self.rotation = 0
        self.rotation_speed = rotation_speed
        self.hitbox_type = "circle"
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)


    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        tooth_len = self.radius*0.3  # 齒的長度
        surface_size = self.radius * 2 + tooth_len * 2
        surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        r = self.radius*0.7
        center = (r + tooth_len, r + tooth_len)
        # 畫每個三角齒
        for i in range(self.teeth):
            angle_deg = self.rotation + (360 / self.teeth) * i
            angle_rad = math.radians(angle_deg)

            # 三角形的三個點
            base_angle1 = angle_rad - math.radians(360 / (2 * self.teeth))  # 左側角
            base_angle2 = angle_rad + math.radians(360 / (2 * self.teeth))  # 右側角
            tip_x = center[0] + math.cos(angle_rad) * (r + tooth_len)
            tip_y = center[1] + math.sin(angle_rad) * (r + tooth_len)
            base1_x = center[0] + math.cos(base_angle1) * r * 0.9
            base1_y = center[1] + math.sin(base_angle1) * r * 0.9
            base2_x = center[0] + math.cos(base_angle2) * r * 0.9
            base2_y = center[1] + math.sin(base_angle2) * r * 0.9

            pygame.draw.polygon(surface, self.color, [
                (base1_x, base1_y),
                (tip_x, tip_y),
                (base2_x, base2_y)
            ])

        # 畫齒輪本體（內圓）
        pygame.draw.circle(surface, self.color, center, r)  # 畫內圓稍大一點
        #pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # 畫黑色邊框表示碰撞箱

        # 畫到主畫面
        screen.blit(surface, (self.x - self.radius, self.y - self.radius))

class FollowGearObstacle(GearObstacle):
    def __init__(self, x, y, radius, player, speed, teeth, rotation_speed=2):
        super().__init__(x, y, radius, 0, 0, teeth, rotation_speed=rotation_speed)
        dx = player.rect.centerx - x
        dy = player.rect.centery - y
        length = max(1, math.hypot(dx, dy))
        vx = dx / length * speed
        vy = dy / length * speed
        self.vx = vx
        self.vy = vy

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)
        self.rotation += self.rotation_speed
        self.rect.center = (self.x, self.y)

class SinGearObstacle(GearObstacle):
    def __init__(self, x, y, radius, vx, vy, amplitude, frequency, teeth, rotation_speed=2):
        super().__init__(x, y, radius, vx, vy, teeth, rotation_speed=rotation_speed)
        self.base_y = y + radius
        self.amplitude = amplitude
        self.frequency = frequency
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.x += self.vx
        t = pygame.time.get_ticks() - self.start_time
        self.y = self.base_y + self.amplitude * math.sin(t * self.frequency)
        self.rotation += self.rotation_speed
        self.rect.center = (self.x, self.y)

class CannonObstacle:
    def __init__(self, x, y, w, h, vx, vy, wave_length=2000, wave_speed=0.05, wave_amplitude=300, num_bars=51):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = vx
        self.vy = vy
        self.rect = pygame.Rect(x, y, w, h)
        self.state = "moving"
        self.expired = False

        self.wave_origin = None
        self.wave_dir = None
        self.wave_length = wave_length
        self.wave_speed = wave_speed
        self.wave_amplitude = wave_amplitude
        self.wave_progress = 0
        self.num_bars = num_bars
        self.wave_rects = []

        self.hitbox_type = "none"
        self.wave_damaged = False
        self.is_collided = False

    def update(self, screen_rect, player):
        if self.state == "moving":
            self.x += self.vx
            self.y += self.vy
            self.rect.topleft = (self.x, self.y)

            if not screen_rect.contains(self.rect):
                self.state = "wave"
                if self.rect.right > screen_rect.right:
                    self.wave_origin = (screen_rect.right, self.rect.centery)
                    self.wave_dir = "left"
                elif self.rect.left < screen_rect.left:
                    self.wave_origin = (screen_rect.left, self.rect.centery)
                    self.wave_dir = "right"
                elif self.rect.bottom > screen_rect.bottom:
                    self.wave_origin = (self.rect.centerx, screen_rect.bottom)
                    self.wave_dir = "up"
                elif self.rect.top < screen_rect.top:
                    self.wave_origin = (self.rect.centerx, screen_rect.top)
                    self.wave_dir = "down"

        elif self.state == "wave":
            self.wave_progress += self.wave_speed
            if self.wave_progress >= 2.35:
                self.expired = True
                self.state = "done"
            else:
                self.generate_wave_rects()
                self.check_player_hit(player)

    def generate_wave_rects(self):
        self.wave_rects = []
        for i in range(self.num_bars):
            dis = abs(i - self.num_bars / 2)
            arrived = (self.wave_progress * 20 / (dis + 1) > 1.5)
            phase = dis / (self.num_bars-1) * math.pi * 5
            decay = 1 - dis / self.num_bars * 1
            passed = dis + 10 > self.wave_progress * 8
            height = math.sin(self.wave_progress * math.pi - phase) * self.wave_amplitude * decay * arrived * passed
            bar_length = self.wave_length / self.num_bars

            if self.wave_dir in ("up", "down"):
                if self.wave_dir == "down":
                    x = self.wave_origin[0] + i * bar_length - self.num_bars * bar_length / 2
                    y = self.wave_origin[1] - height / 2
                else:
                    x = self.wave_origin[0] - i * bar_length + self.num_bars * bar_length / 2
                    y = self.wave_origin[1] - height / 2
                rect = pygame.Rect(x, y, bar_length - 2, height)

            else:  
                if self.wave_dir == "left":
                    x = self.wave_origin[0] - height / 2
                    y = self.wave_origin[1] + i * bar_length - self.num_bars * bar_length / 2
                else:
                    x = self.wave_origin[0] - height / 2
                    y = self.wave_origin[1] - i * bar_length + self.num_bars * bar_length / 2
                rect = pygame.Rect(x, y, height, bar_length - 2)

            self.wave_rects.append(rect)

    def check_player_hit(self, player):
        if self.wave_damaged or not player.alive or player.dashing:
            return
        for rect in self.wave_rects:
            if player.rect.colliderect(rect):
                # player.alive = False
                effect.hurt(self)
                player.blood = player.blood - 10
                self.wave_damaged = True   

    def draw(self, screen):
        if self.state == "moving":
            pygame.draw.rect(screen, (255, 100, 50), self.rect)
        elif self.state == "wave":
            for rect in self.wave_rects:
                pygame.draw.rect(screen, (255, 0, 0), rect) 