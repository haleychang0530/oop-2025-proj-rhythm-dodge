import pygame
import math
import effect
import random

class Obstacle:
    def __init__(self, x, y, w, h, vx, vy):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 50, 50)
        self.vx = vx
        self.vy = vy
        self.shake_duration = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, screen):
        # Apply shake offset if active
        offset_x, offset_y = 0, 0
        if self.shake_duration > 0:
            magnitude = 10  # Shake intensity
            offset_x = random.randint(-magnitude, magnitude)
            offset_y = random.randint(-magnitude, magnitude)
            self.shake_duration -= 1
        else:
            offset_x = 0
            offset_y = 0
        # Draw the obstacle with the shake offset
        shaken_rect = self.rect.copy()
        shaken_rect.x += offset_x
        shaken_rect.y += offset_y
        # Draw the rectangle with the current color
        pygame.draw.rect(screen, self.color, shaken_rect)
        # 如果震動結束，重置shake_duration
        if self.shake_duration <= 0:
            self.shake_duration = 0

    def shake(self, duration=20):
        """開始震動，持續duration幀"""
        self.shake_duration = duration

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
    def __init__(self, x, y, w, h, vx, vy, charge_time, duration = 300):
        super().__init__(x, y, w, h, vx, vy)
        self.charge_time = charge_time
        self.duration = duration
        self.spawn_time = pygame.time.get_ticks() 
        self.activated = False
        self.expired = False
        self.effect_playing = False  # 用於控制音效播放


        # 預熱階段變數
        self.stage = 0
        self.alpha = 0
        self.line_width = 2
        self.transition_progress = 0


        #shake
       


    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.spawn_time
        ct = self.charge_time  # 考慮到遊戲速度調整
        if elapsed < ct + self.duration + 200:
            if elapsed < ct - 200:
                # 淡入紅色提示（0 → 80)
                self.stage = 1
                self.alpha = int(80 * (elapsed / (ct - 200)))


            elif elapsed < ct - 160:
                # 消失階段
                self.stage = 2


            elif elapsed < ct:
                # 細白線 → 擴展
                self.stage = 3
                progress = (elapsed - ct + 160) / 160
                max_width = self.rect.width if self.rect.width > self.rect.height else self.rect.height
                self.line_width = int(2 + (max_width - 2) * progress)


            elif elapsed < ct + 100:
                # 白線轉紅線 # 正式啟動
                self.activated = True
                self.activate_time = now
                self.stage = 4
                self.transition_progress = min(1, (elapsed - ct) / 100)


            elif elapsed < ct + self.duration + 200:
                self.stage = 5 # 雷射結束階段
                progress = (elapsed - ct - 100) / (self.duration + 100)
                if progress > 0.7:
                    self.activated = False
                max_width = self.rect.width if self.rect.width > self.rect.height else self.rect.height
                self.line_width = int(max_width * (1 - progress))
        else:
            self.expired = True
       
        if self.activated and not self.effect_playing:
            effect.lazer()
            self.effect_playing = True  # 確保音效只播放一次


    def get_centered_line_rect(self, width):
        """在原本範圍中心生成一個長條雷射區塊（可調整寬度）"""
        if self.rect.width > self.rect.height:
            # 水平雷射（上下擴張）
            h = width
            y = self.rect.centery - h // 2
            return pygame.Rect(0, y - self.rect.top, self.rect.width, h)
        else:
            # 垂直雷射（左右擴張）
            w = width
            x = self.rect.centerx - w // 2
            return pygame.Rect(x - self.rect.left, 0, w, self.rect.height)


    def draw(self, screen):
        shake_magnitude = 30


        if self.shake_duration > 0:
            offset_x = random.randint(-shake_magnitude, shake_magnitude)
            offset_y = random.randint(-shake_magnitude, shake_magnitude)
            self.shake_duration -= 1
        else:
            offset_x = 0
            offset_y = 0


        # Create a laser_surface exactly as in draw()
        laser_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)


        if self.stage == 1:
            color = (255, 0, 0, self.alpha)
            pygame.draw.rect(laser_surface, color, (0, 0, self.rect.width, self.rect.height))


        elif self.stage == 2:
            pass  # no draw


        elif self.stage == 3:
            color = (255, 255, 255, 255)
            rect = self.get_centered_line_rect(self.line_width)
            pygame.draw.rect(laser_surface, color, rect)


        elif self.stage == 4:
            r = 200
            g = int(255 * (1 - self.transition_progress))
            b = int(255 * (1 - self.transition_progress ** (1/2)))
            color = (r, g, b, 255)
            rect = self.get_centered_line_rect(self.rect.width if self.rect.width > self.rect.height else self.rect.height)
            pygame.draw.rect(laser_surface, color, rect)


        elif self.stage == 5:
            color = (200, 0, 0, 255)
            rect = self.get_centered_line_rect(self.line_width)
            pygame.draw.rect(laser_surface, color, rect)


        # Calculate shaken position
        shaken_pos = (self.rect.x + offset_x, self.rect.y + offset_y)


        # Blit the laser surface with shake offsets
        screen.blit(laser_surface, shaken_pos)


class CircleObstacle(Obstacle):
    def __init__(self, x, y, radius, vx, vy):
        super().__init__(x, y, radius * 2, radius * 2, vx, vy)
        self.radius = radius
    def collide(self, player):
        """檢查玩家是否碰撞到圓形障礙物"""
        left_x = player.rect.centerx - player.rect.width / 2
        right_x = player.rect.centerx + player.rect.width / 2
        top_y = player.rect.centery - player.rect.height / 2
        bottom_y = player.rect.centery + player.rect.height / 2
        distance_lefttop = math.hypot(left_x - self.rect.centerx, top_y - self.rect.centery)
        distance_righttop = math.hypot(right_x - self.rect.centerx, top_y - self.rect.centery)
        distance_leftbottom = math.hypot(left_x - self.rect.centerx, bottom_y - self.rect.centery)
        distance_rightbottom = math.hypot(right_x - self.rect.centerx, bottom_y - self.rect.centery)
        distance = min(distance_lefttop, distance_righttop, distance_leftbottom, distance_rightbottom)
        return distance <= self.radius
    
    #def draw(self, screen):
        #pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
    
    def draw(self, screen):
        # Apply shake offset if active
        offset_x, offset_y = 0, 0
        if self.shake_duration > 0:
            magnitude = 10  # Shake intensity
            offset_x = random.randint(-magnitude, magnitude)
            offset_y = random.randint(-magnitude, magnitude)
            self.shake_duration -= 1
        else:
            offset_x = 0
            offset_y = 0
        # Draw the obstacle with the shake offset
        shaken_rect = self.rect.copy()
        shaken_rect.x += offset_x
        shaken_rect.y += offset_y
        # Draw the rectangle with the current color
        pygame.draw.circle(screen, self.color, shaken_rect.center, self.radius)
        # 如果震動結束，重置shake_duration
        if self.shake_duration <= 0:
            self.shake_duration = 0

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

        #shake
        self.shake_direction=0

    def update(self):
        super().update()
        t = pygame.time.get_ticks() - self.start_time
        self.rect.y = self.base_y + self.amplitude * math.sin(t * self.frequency)

class LaserCircleObstacle(CircleObstacle):
    def __init__(self, x, y, radius, vx, vy, charge_time, duration=300):
        super().__init__(x, y, radius, vx, vy)
        self.charge_time = charge_time
        self.duration = duration
        self.spawn_time = pygame.time.get_ticks()
        self.activated = False
        self.expired = False
        self.stage = 0
        self.alpha = 0
        self.line_width = 2
        self.transition_progress = 0
        self.effect_playing = False

        #shake
        self.shake_direction=0


    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.spawn_time
        ct = self.charge_time

        if elapsed < ct + self.duration + 200:
            if elapsed < ct - 200:
                self.stage = 1
                self.alpha = int(80 * (elapsed / (ct - 200)))

            elif elapsed < ct - 160:
                self.stage = 2

            elif elapsed < ct:
                self.stage = 3
                progress = (elapsed - ct + 160) / 160
                max_width = self.radius * 2
                self.line_width = int(2 + (max_width - 2) * progress)

            elif elapsed < ct + self.duration:
                self.stage = 4
                self.activated = True
                self.activate_time = now
                self.transition_progress = min(1, (elapsed - ct) / self.duration)

            elif elapsed < ct + self.duration + 100:
                self.stage = 5
                progress = (elapsed - ct - self.duration ) / 100
                if progress > 0.7:
                    self.activated = False
                max_width = self.radius * 2
                self.line_width = max_width * (1 - progress)
        else:
            self.expired = True

        if self.activated and not self.effect_playing:
            effect.lazer()
            self.effect_playing = True

    def draw(self, screen):
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        if self.stage == 1:
            color = (255, 0, 0, self.alpha)
            pygame.draw.circle(surface, color, (self.radius, self.radius), self.radius)

        elif self.stage == 2:
            pass

        elif self.stage == 3:
            color = (255, 255, 255, 255)
            pygame.draw.circle(surface, color, (self.radius, self.radius), self.line_width // 2)

        elif self.stage == 4:
            r = 200
            g = int(255 * (1 - self.transition_progress))
            b = int(255 * (1 - self.transition_progress**(1/2)))
            color = (r, g, b, 255)
            pygame.draw.circle(surface, color, (self.radius, self.radius), self.radius)

        elif self.stage == 5:
            color = (200, 0, 0, 255)
            pygame.draw.circle(surface, color, (self.radius, self.radius), self.line_width // 2)

        screen.blit(surface, self.rect.topleft)

class GearObstacle(CircleObstacle):
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
        self.shake_duration = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed
        self.rect.center = (self.x, self.y)
        
        # Shake countdown
        if self.shake_duration > 0:
            self.shake_duration -= 1

    def shake(self, duration=30):
        self.shake_duration = duration  # duration in frames

    def draw(self, screen):
        # Apply shake offset if active
        offset_x, offset_y = 0, 0
        if self.shake_duration > 0:
            magnitude = 10  # Shake intensity
            offset_x = random.randint(-magnitude, magnitude)
            offset_y = random.randint(-magnitude, magnitude)

        tooth_len = self.radius * 0.3
        surface_size = self.radius * 2 + tooth_len * 2
        surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        r = self.radius * 0.7
        center = (r + tooth_len, r + tooth_len)

        for i in range(self.teeth):
            angle_deg = self.rotation + (360 / self.teeth) * i
            angle_rad = math.radians(angle_deg)
            base_angle1 = angle_rad - math.radians(360 / (2 * self.teeth))
            base_angle2 = angle_rad + math.radians(360 / (2 * self.teeth))

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

        pygame.draw.circle(surface, self.color, center, r)

        # Draw to screen with shake offset
        draw_x = self.x - self.radius + offset_x
        draw_y = self.y - self.radius + offset_y
        screen.blit(surface, (draw_x, draw_y))


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
        self.base_x = x + radius
        self.amplitude = amplitude
        self.frequency = frequency
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.x += self.vx
        self.y += self.vy
        t = pygame.time.get_ticks() - self.start_time
        if abs(self.vx) > abs(self.vy) : 
            self.y = self.base_y + self.amplitude * math.sin(t * self.frequency)
        else:
            self.x = self.base_x + self.amplitude * math.sin(t * self.frequency)
        self.rotation += self.rotation_speed
        self.rect.center = (self.x, self.y)
    

class CannonObstacle:
    def __init__(self, x, y, w, h, vx, vy, wave_amplitude, wave_length, num_bars, wave_speed=0.05):
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

        # 0610
        self.shake_duration = 0

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
            decay = 1 - dis / self.num_bars
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
                effect.hurt(self)
                player.blood -= 1
                self.wave_damaged = True
                # start to shake
                self.shake() 
                
    def draw(self, screen):
        # If shaking, apply shake offsets
        offset_x, offset_y = 0, 0
        if self.shake_duration > 0:
            shake_magnitude = 20  # adjust for desired intensity
            offset_x = random.randint(-shake_magnitude, shake_magnitude)
            offset_y = random.randint(-shake_magnitude, shake_magnitude)
            self.shake_duration -= 1

        if self.state == "moving":
            shaken_rect = self.rect.copy()
            shaken_rect.x += offset_x
            shaken_rect.y += offset_y
            pygame.draw.rect(screen, (255, 100, 50), shaken_rect)

        elif self.state == "wave":
            for rect in self.wave_rects:
                rect.x += offset_x
                rect.y += offset_y
                pygame.draw.rect(screen, (255, 0, 0), rect)
                
    def shake(self, duration=20):
        """開始震動，持續duration幀"""
        self.shake_duration = duration
        # 震動時也要更新wave_damaged狀態
        self.wave_damaged = False

class RingObstacle(CircleObstacle):
    def __init__(self, x, y, max_radius, duration=1000, thickness=20, vx=0, vy=0, fade_out=False):
        super().__init__(x, y, 0, vx, vy)
        self.center_pos = pygame.Vector2(x, y)
        self.max_radius = max_radius
        self.duration = duration
        self.thickness = thickness
        self.fade_out = fade_out
        self.rect = pygame.Rect(x - max_radius, y - max_radius, max_radius * 2, max_radius * 2)

        self.spawn_time = pygame.time.get_ticks()
        self.expired = False
        self.alpha = 255
        self.radius = 1  # 避免初始為 0 無法繪製

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.spawn_time

        if elapsed >= self.duration:
            self.expired = True
            return

        progress = elapsed / self.duration
        self.radius = int(self.max_radius * progress)
        self.alpha = int(255 * (1 - progress)) if self.fade_out else 255

        # 更新中心位置
        self.center_pos += pygame.Vector2(self.vx, self.vy)

    def draw(self, screen):
        if self.radius <= 0:
            return  # 不畫
        
        # Make it shake
        # Apply shake offset if active
        offset_x, offset_y = 0, 0
        if self.shake_duration > 0:
            magnitude = 10  # Shake intensity
            offset_x = random.randint(-magnitude, magnitude)
            offset_y = random.randint(-magnitude, magnitude)

        surface_size = self.radius * 2 + self.thickness
        surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        center = (surface.get_width() // 2, surface.get_height() // 2)

        pygame.draw.circle(
            surface,
            (255, 0, 0, self.alpha),
            center,
            self.radius,
            self.thickness
        )

        screen.blit(surface, (
            self.center_pos.x - center[0] + offset_x ,
            self.center_pos.y - center[1] + offset_y
        ))

    def collide(self, player):
        """圓環與玩家碰撞檢查：只判定是否落在圓環邊界區段內"""
        player_corner1 = (player.rect.left, player.rect.top)
        player_corner2 = (player.rect.right, player.rect.bottom)
        player_corner3 = (player.rect.left, player.rect.bottom)
        player_corner4 = (player.rect.right, player.rect.top)
        dist1 = pygame.math.Vector2(player_corner1).distance_to(self.center_pos)
        dist2 = pygame.math.Vector2(player_corner2).distance_to(self.center_pos)
        dist3 = pygame.math.Vector2(player_corner3).distance_to(self.center_pos)
        dist4 = pygame.math.Vector2(player_corner4).distance_to(self.center_pos)
        dist_min = min(dist1, dist2, dist3, dist4)
        dist_max = max(dist1, dist2, dist3, dist4)
        # 檢查是否在圓環的內外半徑之間

        inner = self.radius - self.thickness
        outer = self.radius
        return inner <= dist_min <= outer or inner <= dist_max <= outer 

