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
pygame.display.set_caption("Waveform Beat Visualizer")
clock = pygame.time.Clock()

# === Music setup ===
pygame.mixer.init()
pygame.mixer.music.load("000.wav")
pygame.mixer.music.play()
start_time = time.time()

# === Waveform setup ===
NUM_POINTS = 200  # Number of points in the waveform
point_spacing = WIDTH / NUM_POINTS
wave_heights = [HEIGHT // 2] * NUM_POINTS  # Start flat at middle
wave_speeds = [0] * NUM_POINTS

# === Beat pointer ===
beat_index = 0

# === Main loop ===
running = True
while running:
    screen.fill((0, 0, 0))
    now = time.time() - start_time

    # Handle exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Trigger beat ripple on waveform
    if beat_index < len(beats) and now >= beats[beat_index]:
        center = random.randint(10, NUM_POINTS - 10)
        for offset in range(-8, 9):
            i = center + offset
            if 0 <= i < NUM_POINTS:
                height_offset = max(60 - abs(offset) * 6, 10)
                direction = random.choice([-1, 1])
                wave_speeds[i] = direction * height_offset * 0.3
        beat_index += 1

    # Update waveform points
    for i in range(NUM_POINTS):
        if abs(wave_speeds[i]) > 0.1:
            wave_heights[i] += wave_speeds[i]
            # spring-back effect
            diff = HEIGHT // 2 - wave_heights[i]
            wave_speeds[i] += diff * 0.05  # spring pull
            wave_speeds[i] *= 0.9  # damping
        else:
            wave_heights[i] = HEIGHT // 2
            wave_speeds[i] = 0

    # Draw waveform
    points = [(i * point_spacing, wave_heights[i]) for i in range(NUM_POINTS)]
    pygame.draw.lines(screen, (255, 255, 255), False, points, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
