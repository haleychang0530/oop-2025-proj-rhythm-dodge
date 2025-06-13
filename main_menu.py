import pygame
import json
import time
import random

def main_menu(screen):
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()

    font_title = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 64)
    font_option = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 36)

    options = ["Level 1", "Level 2"]
    selected = 0

    # === Load beat data ===
    with open("levels/menu_level1_beats.json") as f:
        beats = json.load(f)

    # === Music setup ===
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/level1.mp3")
    pygame.mixer.music.play()
    start_time = time.time()

    # === Line setup ===
    NUM_LINES = 200
    spacing = WIDTH / NUM_LINES
    line_heights = [0.0] * NUM_LINES
    line_speeds = [0.0] * NUM_LINES

    # === Beat pointer ===
    beat_index = 0

    running = True
    while running:
        now = time.time() - start_time

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected + 1

        # 背景清除
        screen.fill((10, 10, 30))

        # 觸發節拍波形
        if beat_index < len(beats) and now >= beats[beat_index]:
            center = random.randint(10, NUM_LINES - 10)
            for offset in range(-8, 9):
                i = center + offset
                if 0 <= i < NUM_LINES:
                    d = abs(offset)
                    amplitude = max(90 - d * 10, 8)
                    line_speeds[i] -= amplitude
            beat_index += 1

        # 波形物理更新
        for i in range(NUM_LINES):
            diff = -line_heights[i]
            line_speeds[i] += diff * 0.2
            line_speeds[i] *= 0.85
            line_heights[i] += line_speeds[i]

        # 平滑波形
        smooth_heights = [0.0] * NUM_LINES
        for i in range(NUM_LINES):
            total = 0
            count = 0
            for j in range(-2, 3):
                ni = i + j
                if 0 <= ni < NUM_LINES:
                    total += line_heights[ni]
                    count += 1
            smooth_heights[i] = total / count

        # 繪製波形（線條從底部往上）
        for i in range(NUM_LINES):
            x = i * spacing
            height = smooth_heights[i]
            y1 = HEIGHT - height * 2
            y2 = HEIGHT
            pygame.draw.line(screen, (255, 255, 255), (x, y1), (x, y2), 2)

        # 繪製標題
        title = font_title.render("RHYTHM DODGE", True, (0, 200, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # 繪製選單選項
        for i, text in enumerate(options):
            color = (255, 255, 255) if i == selected else (150, 150, 150)
            label = font_option.render(text, True, color)
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 250 + i * 60))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return None
