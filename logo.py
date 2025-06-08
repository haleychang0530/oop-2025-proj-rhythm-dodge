import pygame
import math

def draw_logo(screen, time):
    screen_width, screen_height = screen.get_size()
    # 漸變顏色函式（從深藍到淺藍漸變）
    def gradient_color(t):
        # t 是 0~1 浮點數，返回 RGB
        start_color = pygame.Color(0, 100, 150)
        end_color = pygame.Color(0, 200, 255)
        r = start_color.r + (end_color.r - start_color.r) * t
        g = start_color.g + (end_color.g - start_color.g) * t
        b = start_color.b + (end_color.b - start_color.b) * t
        return (int(r), int(g), int(b))

    # 動態顏色變化（0~1 周期變化）
    pulse = (math.sin(time * 2) + 1) / 2  # 0~1 間震盪

    font = pygame.font.SysFont("Arial", 72, bold=True)
    title_color = gradient_color(pulse)
    title = font.render("Rhythm Dodge", True, title_color)

    # 文字輕微上下擺動動畫
    y_offset = 10 * math.sin(time * 3)

    subtitle_font = pygame.font.SysFont("Arial", 32, italic=True)
    subtitle = subtitle_font.render("Dodge the beat. Feel the rhythm.", True, (255, 255, 255))

    # 中心置中
    title_rect = title.get_rect(center=(screen_width // 2, screen_height // 3 + y_offset))
    subtitle_rect = subtitle.get_rect(center=(screen_width // 2, screen_height // 3 + 80 + y_offset))

    # 畫文字陰影（讓字體有點立體感）
    shadow_offset = 3
    shadow_color = (20, 20, 20)
    shadow_title = font.render("Rhythm Dodge", True, shadow_color)
    shadow_subtitle = subtitle_font.render("Dodge the beat. Feel the rhythm.", True, shadow_color)

    screen.blit(shadow_title, (title_rect.x + shadow_offset, title_rect.y + shadow_offset))
    screen.blit(shadow_subtitle, (subtitle_rect.x + shadow_offset, subtitle_rect.y + shadow_offset))

    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)

# --- 測試用 ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Logo")

    clock = pygame.time.Clock()
    running = True
    start_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        now = pygame.time.get_ticks()
        elapsed_sec = (now - start_time) / 1000  # 秒

        draw_logo(screen, elapsed_sec)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
