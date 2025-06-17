import aubio
import numpy as np
import pygame
import time

# === Aubio setup ===
win_s = 1024  # window size for FFT
hop_s = 512   # hop size
source = aubio.source("level2.ogg", 0, hop_s)  # 0 means autodetect sample rate
samplerate = source.samplerate
tempo = aubio.tempo("default", win_s, hop_s, samplerate)

# === Pygame setup ===
pygame.init()
pygame.mixer.init(frequency=samplerate)
pygame.mixer.music.load("level2.ogg")
pygame.mixer.music.play()

# === Beat detection loop ===
beats = []
total_frames = 0

print("Detecting beats in real-time...")

while True:
    samples, read = source()
    is_beat = tempo(samples)
    if is_beat:
        beat_time = total_frames / float(samplerate)
        beats.append(beat_time)
        print("Beat at:", round(beat_time, 3), "seconds")
    total_frames += read
    if read < hop_s:
        break

print("Done! Total beats:", len(beats))

import json

# 儲存 beat 資料成 JSON 檔
with open("level2_beats.json", "w") as f:
    json.dump(beats, f, indent=2)

print("Saved to level2_beats.json")
