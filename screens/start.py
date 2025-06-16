import pygame
import math
import sys

def start(screen):
    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 58, 111) # origianl: (200, 0, 0)
    BLUE = (0, 215, 237) #original; (0, 200, 255)

    #font = pygame.font.SysFont("Arial", 80, bold=True)
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 80)
    small_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 30)


    gear_center = (175, 269)
    gear_radius = 25
    gear_teeth = 12
    gear_angle = 0
    triangle_offset = 0
    triangle_direction = 1

    def draw_text():
        screen.blit(font.render("R", True, WHITE), (50, 100))
        screen.blit(font.render("H", True, WHITE), (120, 100))
        screen.blit(font.render("Y", True, WHITE), (190, 100))
        screen.blit(font.render("T", True, WHITE), (260, 100))
        screen.blit(font.render("H", True, WHITE), (330, 100))
        screen.blit(font.render("M", True, WHITE), (400, 100))
        screen.blit(font.render("D", True, WHITE), (80, 220))
        screen.blit(font.render("DGE", True, WHITE), (200, 220))

    def draw_triangles(offset):
        pygame.draw.polygon(screen, RED, [
            (202, 120 + offset),
            (222, 140 + offset),
            (242, 120 + offset)
        ])
        
    
    def draw_retangle(x, y, width, height, color):
        pygame.draw.rect(screen, color, (x, y, width, height))

    def draw_gear(center, radius, teeth, angle):
        points = []
        for i in range(teeth * 2):
            theta = angle + i * math.pi / teeth
            r = radius if i % 2 == 0 else radius * 0.7
            x = center[0] + r * math.cos(theta)
            y = center[1] + r * math.sin(theta)
            points.append((x, y))
        pygame.draw.polygon(screen, WHITE, points)

    # === MAIN LOOP ===

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  

        screen.fill(BLACK)
        draw_text()
        draw_triangles(triangle_offset)
        draw_retangle(345, 157, 38, 24, BLUE)
        draw_gear(gear_center, gear_radius, gear_teeth, gear_angle)

        # "Press ENTER to continue" text
        enter_text = small_font.render("Press ENTER to continue", True, WHITE)
        screen.blit(enter_text, (250, 500))

        # Proper animation logic
        triangle_offset += triangle_direction * 0.5
        if triangle_offset > 5 or triangle_offset < -5:
            triangle_direction *= -1

        gear_angle += 0.05
        pygame.display.flip()
        clock.tick(60)
