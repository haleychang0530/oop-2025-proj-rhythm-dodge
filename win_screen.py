import pygame
import random
import sys
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Victory Screen")
clock = pygame.time.Clock()

# === Fonts and Colors ===
font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 64)
WHITE = (255, 255, 255)
BG_COLOR = (10, 10, 30)

# === 資料結構 ===
class Note:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(1.5, 4.5)
        self.size = random.randint(18, 36)
        self.char = random.choice(["|", "."])
        self.color = random.choice([
            (255, 255, 255)
        ])
        self.font = pygame.font.SysFont("Arial", self.size, bold=True)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.__init__()

    def draw(self, surface):
        label = self.font.render(self.char, True, self.color)
        surface.blit(label, (self.x, self.y))

# === 初始化音符 ===
notes = [Note() for _ in range(50)]

# === 音效（可選）===
# pygame.mixer.init()
# pygame.mixer.Sound("assets/sfx/victory.wav").play()

def victory_screen():
    start_time = time.time()
    timer = 0
    running = True
    while running:
        screen.fill(BG_COLOR)
        timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False

        # 自動跳轉：顯示 2 秒後返回
        if time.time() - start_time > 5:
            return  # 自動返回主選單

        # 更新與畫出音符
        for note in notes:
            note.update()
            note.draw(screen)

        # 顯示主文字
        if timer < 60:
            alpha = min(255, timer * 5)
        else:
            alpha = 255
        title_surf = font.render("victory!", True, WHITE)
        title_surf.set_alpha(alpha)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 2 - 50))

        pygame.display.flip()
        clock.tick(60)

