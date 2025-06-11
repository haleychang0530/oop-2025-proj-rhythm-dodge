import pygame
import random
import sys
import math

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Entrance Effect")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AURA_COLOR = (200, 100, 255)

# Boss placeholder sprite
boss_img = pygame.Surface((200, 200), pygame.SRCALPHA)
pygame.draw.circle(boss_img, (150, 0, 150), (100, 100), 100)

# Shake effect
class Shake:
    def __init__(self, duration=400, intensity=10):
        self.duration = duration
        self.time_left = duration
        self.intensity = intensity
        self.offset = (0, 0)
    
    def update(self, dt):
        if self.time_left > 0:
            self.time_left -= dt
            self.offset = (
                random.randint(-self.intensity, self.intensity),
                random.randint(-self.intensity, self.intensity)
            )
        else:
            self.offset = (0, 0)

# Flash effect
class Flash:
    def __init__(self, duration=200):
        self.duration = duration
        self.time_left = duration
    
    def update(self, dt):
        self.time_left = max(0, self.time_left - dt)
    
    def draw(self, surface):
        if self.time_left > 0:
            alpha = int(255 * (self.time_left / self.duration))
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, alpha))
            surface.blit(overlay, (0, 0))

# Pulsing aura
class PulseAura:
    def __init__(self, max_radius=180, speed=0.005):
        self.max_radius = max_radius
        self.speed = speed
        self.progress = 0
    
    def update(self, dt):
        self.progress = (self.progress + dt * self.speed) % (2 * math.pi)
    
    def draw(self, surface, center):
        alpha = int(100 + 80 * math.sin(self.progress))
        color = (*AURA_COLOR, alpha)
        aura = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(aura, color, (self.max_radius, self.max_radius), self.max_radius)
        surface.blit(aura, (center[0] - self.max_radius, center[1] - self.max_radius), special_flags=pygame.BLEND_PREMULTIPLIED)

# Boss position
boss_pos = (WIDTH // 2, HEIGHT // 2)

# Effects
shake = Shake()
flash = Flash()
aura = PulseAura()

# Simulate boss entrance every 3 seconds
pygame.time.set_timer(pygame.USEREVENT, 3000)

# Game loop
running = True
while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            shake = Shake(500, intensity=20)
            flash = Flash(300)

    # Update effects
    shake.update(dt)
    flash.update(dt)
    aura.update(dt)

    # Draw to temporary surface
    temp_surface = pygame.Surface((WIDTH, HEIGHT))
    temp_surface.fill(BLACK)

    # Draw aura and boss
    aura.draw(temp_surface, boss_pos)
    temp_surface.blit(boss_img, (boss_pos[0] - 100, boss_pos[1] - 100))

    # Flash overlay
    flash.draw(temp_surface)

    # Final blit with shake
    screen.fill(BLACK)
    screen.blit(temp_surface, shake.offset)
    pygame.display.flip()

pygame.quit()
sys.exit()

