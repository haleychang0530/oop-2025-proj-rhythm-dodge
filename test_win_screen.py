import pygame
from win_screen import victory_screen

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Victory Screen Test")

victory_screen(screen)  # test it directly

pygame.quit()
