import pygame
import math
import sys

# 初始化
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rhythm Dodge Logo")
clock = pygame.time.Clock()

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 200, 255)

# 字體設定
font = pygame.font.SysFont("Arial", 80, bold=True)

# 齒輪參數
gear_center = (167, 253)
gear_radius = 25
gear_teeth = 12
gear_angle = 0

# 三角形動畫參數
triangle_offset = 0
triangle_direction = 1

def draw_text():
    # 畫出上排 RH_THM
    screen.blit(font.render("R", True, WHITE), (50, 100))
    screen.blit(font.render("H", True, WHITE), (120, 100))
    screen.blit(font.render("Y", True, WHITE), (190, 100))
    screen.blit(font.render("T", True, WHITE), (260, 100))
    screen.blit(font.render("H", True, WHITE), (330, 100))
    screen.blit(font.render("M", True, WHITE), (400, 100))
    
    
    # 畫出下排 D DGE（中間那顆齒輪的位置留空）
    screen.blit(font.render("D", True, WHITE), (80, 220))
    screen.blit(font.render("DGE", True, WHITE), (200, 220))

def draw_triangles():
    # Y 的紅色倒三角
    pygame.draw.polygon(screen, RED, [
        (200, 100 + triangle_offset),
        (230, 100 + triangle_offset),
        (215, 130 + triangle_offset)
    ])
    
    # M 的藍色直立三角
    pygame.draw.polygon(screen, BLUE, [
        (453, 123 + triangle_offset),
        (453, 170 + triangle_offset),
        (438, 170 + triangle_offset)
    ])

def draw_gear(center, radius, teeth, angle):
    points = []
    for i in range(teeth * 2):
        theta = angle + i * math.pi / teeth
        r = radius if i % 2 == 0 else radius * 0.7
        x = center[0] + r * math.cos(theta)
        y = center[1] + r * math.sin(theta)
        points.append((x, y))
    pygame.draw.polygon(screen, WHITE, points)

# 主迴圈
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    draw_text()
    draw_triangles()
    draw_gear(gear_center, gear_radius, gear_teeth, gear_angle)

    # 更新動畫參數
    triangle_offset += triangle_direction * 0.5
    if triangle_offset > 5 or triangle_offset < -5:
        triangle_direction *= -1

    gear_angle += 0.05

    pygame.display.flip()
    clock.tick(60)
