import pygame
import random

class Particle:
    def __init__(self, x, y, color=(255, 80, 80), size=None, life=30):
        self.pos = [x, y]
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.life = life
        self.color = color
        self.size = size or random.randint(2, 5)
        self.max_life = life



    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            surf.fill((*self.color, alpha))
            screen.blit(surf, self.pos)