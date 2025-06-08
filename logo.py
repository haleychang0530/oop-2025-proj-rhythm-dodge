import pygame
import math

pygame.init()
screen = pygame.display.set_mode((700, 200))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 80)

# GearObstacle class (simplified spinning gear)
class GearObstacle():
    def __init__(self, x, y, radius, rotation_speed=5, teeth=12, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.rotation = 0
        self.rotation_speed = rotation_speed
        self.teeth = teeth
        self.color = color

    def update(self):
        self.rotation = (self.rotation + self.rotation_speed) % 360

    def draw(self, screen, pos):
        tooth_len = self.radius * 0.3
        surface_size = int(self.radius * 2 + tooth_len * 2)
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
            pygame.draw.polygon(surface, self.color, [(base1_x, base1_y), (tip_x, tip_y), (base2_x, base2_y)])
        pygame.draw.circle(surface, self.color, center, r)
        screen.blit(surface, (pos[0] - self.radius - tooth_len, pos[1] - self.radius - tooth_len))

# 文字和对应的绘制风格函数
def draw_normal(screen, letter, pos, color=(255,255,255)):
    surf = font.render(letter, True, color)
    screen.blit(surf, pos)

def draw_shadow(screen, letter, pos, color=(255,255,255)):
    # 先画阴影
    shadow_surf = font.render(letter, True, (0,200,255))
    screen.blit(shadow_surf, (pos[0]+3, pos[1]+3))
    # 再画文字
    surf = font.render(letter, True, color)
    screen.blit(surf, pos)

def draw_gradient(screen, letter, pos):
    # 简单用渐变色文字（先渲染白色，再用半透明矩形做渐变叠加）
    surf = font.render(letter, True, (255, 255, 255))
    grad = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    width, height = surf.get_size()
    for i in range(height):
        alpha = int(255 * i / height)
        pygame.draw.line(grad, (200, 0, 0, alpha), (0, i), (width, i))
    surf.blit(grad, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(surf, pos)

# 创建旋转齿轮实例
gear = GearObstacle(0, 0, 25, rotation_speed=5, teeth=12, color=(255, 255, 255))

text = "Rhythm Dodge"
# 每个字母对应绘制风格id: 0-普通, 1-阴影, 2-渐变, 3-齿轮
styles = [0, 1, 0, 2, 0, 1, 0, 0, 3, 0, 0, 0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 20))

    gear.update()

    x = 50
    y = 100
    spacing = 55

    for i, letter in enumerate(text):
        style = styles[i]
        pos = (x + i * spacing, y)

        if style == 0:
            draw_normal(screen, letter, pos)
        elif style == 1:
            draw_shadow(screen, letter, pos)
        elif style == 2:
            draw_gradient(screen, letter, pos)
        elif style == 3:
            # 齿轮只用来绘制字母O，位置传进去
            if letter.upper() == "O":
                gear.draw(screen, (pos[0] + 20, pos[1] + 20))
            else:
                draw_normal(screen, letter, pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
