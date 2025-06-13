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
pygame.display.set_caption("Bar Chart Beat Ripple")
clock = pygame.time.Clock()

# === Music setup ===
pygame.mixer.init()
pygame.mixer.music.load("000.wav")
pygame.mixer.music.play()
start_time = time.time()

# === Bar setup ===
NUM_BARS = 80  # More bars, thinner width
bar_width = WIDTH / NUM_BARS
bar_heights = [0] * NUM_BARS
bar_speeds = [0] * NUM_BARS

# === Beat pointer ===
beat_index = 0

# === Main loop ===
running = True
while running:
    screen.fill((10, 10, 10))
    now = time.time() - start_time

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Detect beat and trigger bar spikes
    if beat_index < len(beats) and now >= beats[beat_index]:
        # Select center index and apply ripple outward
        center = random.randint(10, NUM_BARS - 10)
        for offset in range(-4, 5):  # ripple range
            i = center + offset
            if 0 <= i < NUM_BARS:
                height = max(150 - abs(offset) * 25, 30)
                bar_heights[i] = height
                bar_speeds[i] = -6
        beat_index += 1

    # Update and draw bars
    for i in range(NUM_BARS):
        if bar_heights[i] > 0 or bar_speeds[i] < 0:
            bar_speeds[i] += 0.7  # gravity
            bar_heights[i] += bar_speeds[i]
            if bar_heights[i] < 0:
                bar_heights[i] = 0
                bar_speeds[i] = 0

        x = i * bar_width
        y = HEIGHT - bar_heights[i]
        pygame.draw.rect(screen, (0, 200, 255), (x, y, bar_width, bar_heights[i]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
