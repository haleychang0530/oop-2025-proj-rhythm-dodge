import pygame
import math

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (0, 215, 237) # original: (0, 200, 255)
        self.speed = 5
        self.alive = True
        self.dash_speed = 50
        self.dash_cooldown = 500  # 500 毫秒
        self.last_dash_time = -self.dash_cooldown
        self.dash_direction = [0, 0]
        self.dashing = False
        self.dash_vector = [0, 0]
        self.dash_start_time = 0
        self.dash_duration = 150  # 0.15 秒
        self.dash_speed_multiplier = 1000 / self.dash_duration
        self.damage_cooldown = 100
        self.damaged = 0
        self.allow_damage = 1
        self.damage_time = 0

        self.blood = 100

    def update(self, keys):

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
                self.color = (0, 215, 237)  # 恢復原色 # original: (0, 200, 255) 
            else:
                # 計算速度衰減（線性衰減）
                t = elapsed / self.dash_duration  # 0.0 ~ 1.0
                speed = self.speed * (self.dash_speed_multiplier * (1 - t) + t) 
                # 更新位置
                self.rect.x += self.dash_vector[0] * speed
                self.rect.y += self.dash_vector[1] * speed
                self.color = (255, 255, 255)
                self.rect.clamp_ip(pygame.Rect(5, 5, 790, 590))
                return  # dash 中不接受其他移動輸入

        #damage    
        if self.damaged:
            self.damage_time = now
            self.damaged = 0
        
        if self.damage_cooldown < now - self.damage_time:
            self.allow_damage = 1
        else:
            self.allow_damage = 0

                

        # 一般移動（未衝刺時）
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # 限制在邊界內
        self.rect.clamp_ip(pygame.Rect(5, 5, 790, 590))



    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect)

            # === 眼睛邏輯（方形）===
            eye_size = 6
            padding_x = 5
            padding_y = 10

            keys = pygame.key.get_pressed()
            eye_offset_x = 3 if keys[pygame.K_RIGHT] else (-3 if keys[pygame.K_LEFT] else 0)
            eye_offset_y = 3 if keys[pygame.K_DOWN] else (-3 if keys[pygame.K_UP] else 0)

            now = pygame.time.get_ticks()
            blink_cycle = 3000  # 每 2 秒
            blink_duration = 150
            blinking = (now % blink_cycle) < blink_duration

            eye1_x = self.rect.x + padding_x + eye_offset_x
            eye1_y = self.rect.y + padding_y + eye_offset_y
            eye2_x = self.rect.x + self.rect.width - padding_x - eye_size + eye_offset_x
            eye2_y = eye1_y

            eye_color = (0, 60, 60)

            if blinking:
                # 眨眼畫細橫線
                pygame.draw.line(screen, eye_color, (eye1_x, eye1_y + eye_size // 2), (eye1_x + eye_size, eye1_y + eye_size // 2), 2)
                pygame.draw.line(screen, eye_color, (eye2_x, eye2_y + eye_size // 2), (eye2_x + eye_size, eye2_y + eye_size // 2), 2)
            else:
                # 正常方形眼睛
                pygame.draw.rect(screen, eye_color, (eye1_x, eye1_y, eye_size, eye_size))
                pygame.draw.rect(screen, eye_color, (eye2_x, eye2_y, eye_size, eye_size))

        else:
            # 死亡狀態：灰身體 + 閉眼（橫線）
            pygame.draw.rect(screen, (100, 100, 100), self.rect)

            eye_size = 6
            padding_x = 6
            padding_y = 10

            eye1_x = self.rect.x + padding_x
            eye1_y = self.rect.y + padding_y
            eye2_x = self.rect.x + self.rect.width - padding_x - eye_size
            eye2_y = eye1_y

            eye_color = (50, 50, 50)
            pygame.draw.line(screen, eye_color, (eye1_x, eye1_y + eye_size // 2), (eye1_x + eye_size, eye1_y + eye_size // 2), 2)
            pygame.draw.line(screen, eye_color, (eye2_x, eye2_y + eye_size // 2), (eye2_x + eye_size, eye2_y + eye_size // 2), 2)
