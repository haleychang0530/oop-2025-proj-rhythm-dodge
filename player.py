import pygame
import math

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (0, 200, 255)
        self.speed = 5
        self.alive = True
        self.dash_speed = 50
        self.dash_cooldown = 1000  # 毫秒
        self.last_dash_time = -self.dash_cooldown
        self.dash_direction = [0, 0]
        self.dashing = False
        self.dash_vector = [0, 0]
        self.dash_start_time = 0
        self.dash_duration = 200  # 0.5 秒
        self.dash_speed_multiplier = 5

        # 0612 改:血條
        self.blood = 100

    def update(self, keys):

        # 0607 小改:血條
        if self.blood <= 0:
            self.alive = False

        if not self.alive:
            return

        now = pygame.time.get_ticks()
        dx, dy = 0, 0

        # 控制方向
        if keys[pygame.K_LEFT]: dx -= 1
        if keys[pygame.K_RIGHT]: dx += 1
        if keys[pygame.K_UP]: dy -= 1
        if keys[pygame.K_DOWN]: dy += 1

        # 斜對角修正
        if dx != 0 and dy != 0:
            dx *= math.sqrt(2) / 2
            dy *= math.sqrt(2) / 2
        

        # 開始衝刺
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and (dx != 0 or dy != 0):
            if now - self.last_dash_time >= self.dash_cooldown and not self.dashing:
                self.last_dash_time = now
                self.dashing = True
                self.dash_start_time = now
                self.dash_vector = [dx, dy]

        # Dash 狀態
        if self.dashing:
            elapsed = now - self.dash_start_time
            if elapsed >= self.dash_duration:
                self.dashing = False
                self.color = (0, 200, 255)  # 恢復原色
            else:
                # 計算速度衰減（線性衰減）
                t = elapsed / self.dash_duration  # 0.0 ~ 1.0
                speed = self.speed * (self.dash_speed_multiplier * (1 - t) + t)  # 10x → 1x
                # 更新位置
                self.rect.x += self.dash_vector[0] * speed
                self.rect.y += self.dash_vector[1] * speed
                self.color = (255, 255, 255)
                self.rect.clamp_ip(pygame.Rect(5, 5, 790, 590))
                return  # dash 中不接受其他移動輸入
                

        # 一般移動（未衝刺時）
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # 限制在邊界內
        self.rect.clamp_ip(pygame.Rect(5, 5, 790, 590))



    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)