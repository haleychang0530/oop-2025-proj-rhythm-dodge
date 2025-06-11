import pygame

def hud(screen, current_health, max_health = 100):

    # Bar dimensions
    bar_x, bar_y = 290, 20
    bar_width, bar_height = 200, 20
    tip_width = 15
    #spacing = 2

    # Colors
    bg_color = (60, 30, 30)          # Dark reddish background
    fill_color = (255, 200, 200)      # Cyan fill
    border_color = (250, 150, 150)     # Darker border
    tip_color = (10, 10, 10)     # Battery tip (grayish)
    cube_width = 15

    if current_health==0:
        fill_color = (255, 0, 0)

    # Background bar
    pygame.draw.rect(screen, bg_color, (bar_x, bar_y, bar_width + 20, bar_height))
    pygame.draw.rect(screen, 	(50, 50, 50)   , (bar_x + cube_width/2 , bar_y + bar_height / 3, bar_width , bar_height / 3))

    # Fill level
    fill_ratio = max(0, min(1, current_health / max_health))
    fill_width = int(bar_width * fill_ratio)
    pygame.draw.rect(screen, fill_color, ( bar_x + bar_width - fill_width, bar_y, cube_width , bar_height))

    # Border
    pygame.draw.rect(screen, border_color, (bar_x , bar_y, bar_width + tip_width, bar_height), 2)

    # Battery tip
    tip_rect = pygame.Rect(bar_x + bar_width + 13, bar_y, tip_width , bar_height)
    pygame.draw.rect(screen, tip_color, tip_rect)

    pygame.draw.polygon(screen, (60,60,60), [(bar_x + bar_width + 25 , bar_y + 2),(bar_x + bar_width + 17, bar_y + 16) ,(bar_x + bar_width + 33, bar_y + 16)], 5)
    
    # 載入圖片
    image = pygame.image.load("assets/images/boss_2.png")
    new_width, new_height = 35, 35
    resized_image = pygame.transform.scale(image, (new_width, new_height))
    # 繪製圖片
    screen.blit(resized_image, (bar_x + bar_width + 7, bar_y - 7))