import pygame
import json
import time
import random

# === Load beat data ===
with open("tutorial_beats.json") as f:
    beats = json.load(f)

# === Pygame setup ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Waveform Vertical Line Visualizer")
clock = pygame.time.Clock()

# === Music setup ===
pygame.mixer.init()
pygame.mixer.music.load("000.wav")
pygame.mixer.music.play()
start_time = time.time()

# === Line setup ===
NUM_LINES = 150
spacing = WIDTH / NUM_LINES
line_heights = [0] * NUM_LINES
line_speeds = [0] * NUM_LINES

# === Beat pointer ===
beat_index = 0

# === Main loop ===
running = True
while running:
    screen.fill((0, 0, 0))
    now = time.time() - start_time

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Beat trigger
    if beat_index < len(beats) and now >= beats[beat_index]:
        center = random.randint(10, NUM_LINES - 10)
        for offset in range(-6, 7):
            i = center + offset
            if 0 <= i < NUM_LINES:
                height_offset = max(80 - abs(offset) * 8, 10)
                line_speeds[i] = -height_offset  # upward
        beat_index += 1

    # Update lines
    for i in range(NUM_LINES):
        if abs(line_speeds[i]) > 0.1:
            line_heights[i] += line_speeds[i]
            diff = 0 - line_heights[i]  # pull back to center
            line_speeds[i] += diff * 0.2  # spring
            line_speeds[i] *= 0.85  # damping
        else:
            line_heights[i] = 0
            line_speeds[i] = 0

    # Draw vertical lines
    for i in range(NUM_LINES):
        x = i * spacing
        y1 = HEIGHT // 2 - line_heights[i]
        y2 = HEIGHT // 2 + line_heights[i]
        pygame.draw.line(screen, (255, 255, 255), (x, y1), (x, y2), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
