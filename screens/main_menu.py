import pygame
import json
import time
import random
from sound_manager import SoundManager

sound_manager = SoundManager()

def main_menu(screen):
    WIDTH, HEIGHT = screen.get_size()
    #pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()

    font_title = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 64)
    font_option = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 36)

    options = ["Level 1", "Level 2"]
    selected = 0
    prev_selected = -1  # to detect changes

    level_info = [
    {"name": "Time Leaper", "author": "Hinkik", "time": "01:08"},
    {"name": "Highscore", "author": "Teminite & Panda Eyes", "time": "01:10"}
    ]

    level_beat_paths = [
        "levels/menu_level1_beats.json",
        "levels/menu_level2_beats.json"
    ]

    level_music_paths = [
        "assets/music/level1.ogg",
        "assets/music/level2.ogg"
    ]
    
    pygame.mixer.music.load(level_music_paths[selected])
    pygame.mixer.music.play(-1)  # Loop the music

    all_beats = []
    for path in level_beat_paths:
        with open(path) as f:
            all_beats.append(json.load(f))

    pygame.mixer.init()

    # === Line setup ===
    NUM_LINES = 200
    spacing = WIDTH / NUM_LINES
    line_heights = [0.0] * NUM_LINES
    line_speeds = [0.0] * NUM_LINES
    beat_index = 0
    start_time = time.time()

    # === Beat pointer ===
    beat_index = 0

    running = True
    while running:
        now = time.time() - start_time
        beats = all_beats[selected]  # Preview the selected level's waveform

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sound_manager.play_sfx("choose_option")
                    sound_manager.set_volume(0.4)
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    sound_manager.play_sfx("choose_option")
                    sound_manager.set_volume(0.4)
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    sound_manager.play_sfx("confirm_option")
                    return selected + 1
                elif event.key == pygame.K_ESCAPE:
                    sound_manager.play_sfx("confirm_option")
                    running = False
                    return None
                
        # Detect level selection change
        if selected != prev_selected:
            sound_manager.stop_music()
            sound_manager.play_music(level_music_paths[selected], loop=-1)
            sound_manager.set_volume(0.4)
            
            start_time = time.time()
            beat_index = 0
            line_heights = [0.0] * NUM_LINES
            line_speeds = [0.0] * NUM_LINES
            prev_selected = selected

        # 背景清除
        screen.fill((10, 10, 30))

        # 顯示選定關卡的資訊
        info_font_name = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 26)
        info_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 22)
        info = level_info[selected]

        name_text = info_font_name.render(f"{info['name']}", True, (200, 200, 255))
        author_text = info_font.render(f"by: {info['author']}", True, (200, 200, 255))
        time_text = info_font.render(f"length: {info['time']}", True, (200, 200, 255))

        #info_x = WIDTH // 2 - name_text.get_width() // 2
        screen.blit(name_text, (400, 250)) #+info_x
        screen.blit(author_text, (400, 300))
        screen.blit(time_text, (400, 330))

        esc_to_exit = info_font.render("Press ESC to exit", True, (200, 200, 200))

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

        pygame.draw.rect(screen, (10, 10, 50), pygame.Rect(0, 0, 800, 600), 5)

        # 繪製標題
        title = font_title.render("RHYTHM DODGE", True, (0, 200, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(esc_to_exit, (WIDTH // 2 - esc_to_exit.get_width() // 2, 500))

        # 繪製選單選項
        for i, text in enumerate(options):
            color = (255, 255, 255) if i == selected else (150, 150, 150)
            label = font_option.render(text, True, color)
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2 - 150, 250 + i * 60))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return None
