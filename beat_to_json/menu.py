import pygame
import json
import time
import random
import math

# === Load beat data ===
with open("tutorial_beats.json") as f:
    beats = json.load(f)

# === Pygame setup ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smooth Waveform Visualizer")
clock = pygame.time.Clock()

# === Music setup ===
pygame.mixer.init()
pygame.mixer.music.load("000.wav")
pygame.mixer.music.play()
start_time = time.time()

# === Line setup ===
NUM_LINES = 200
spacing = WIDTH / NUM_LINES
line_heights = [0.0] * NUM_LINES
line_speeds = [0.0] * NUM_LINES

# === Beat pointer ===
beat_index = 0

# === Main loop ===
running = True
while running:
    screen.fill((0, 0, 0))
    now = time.time() - start_time

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Trigger beat
    if beat_index < len(beats) and now >= beats[beat_index]:
        center = random.randint(10, NUM_LINES - 10)
        for offset in range(-8, 9):
            i = center + offset
            if 0 <= i < NUM_LINES:
                d = abs(offset)
                amplitude = max(90 - d * 10, 8)  # smoother fall-off
                line_speeds[i] -= amplitude
        beat_index += 1

    # Update line heights with smoothing
    for i in range(NUM_LINES):
        # Spring effect
        diff = -line_heights[i]
        line_speeds[i] += diff * 0.2
        line_speeds[i] *= 0.85
        line_heights[i] += line_speeds[i]

    # Smooth neighbor interpolation
    smooth_heights = [0.0] * NUM_LINES
    for i in range(NUM_LINES):
        total = 0
        count = 0
        for j in range(-2, 3):  # 5-point average
            ni = i + j
            if 0 <= ni < NUM_LINES:
                total += line_heights[ni]
                count += 1
        smooth_heights[i] = total / count

    # Draw lines
    for i in range(NUM_LINES):
        x = i * spacing
        height = smooth_heights[i]
        y1 = HEIGHT - height * 2
        y2 = HEIGHT 
        pygame.draw.line(screen, (255, 255, 255), (x, y1), (x, y2), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
