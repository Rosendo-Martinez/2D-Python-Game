import pygame
from Game_Code.Map.Map import *

def getMapColor(m,n):
    sm = -1 if m < 0 else 1
    sn = -1 if n < 0 else 1
    m = math.fabs(m)
    n = math.fabs(n)
    if m % 2 != 0:
        if n % 2 != 0:
            if ((sm == 1 and sn == 1) or (sm == -1 and sn == -1)):
                return 'black'
            else:
                return 'white'
        else:
            if ((sm == 1 and sn == 1) or (sm == -1 and sn == -1)):
                return 'white'
            else:
                return 'black'
    else:
        if n % 2 != 0:
            if ((sm == 1 and sn == 1) or (sm == -1 and sn == -1)):
                return 'white'
            else:
                return 'black'
        else:
            if ((sm == 1 and sn == 1) or (sm == -1 and sn == -1)):
                return 'black'
            else:
                return 'white'


pygame.init()

MAP_WIDTH = 51
MAP_HEIGHT = 53
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BackgroundMap = Map(MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
SPEED = 4

MAPS = ['black','white']

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen_rect_rel_bg = screen.get_rect()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        screen_rect_rel_bg.left -= SPEED
    if keys[pygame.K_d]:
        screen_rect_rel_bg.left += SPEED
    if keys[pygame.K_w]:
        screen_rect_rel_bg.top -= SPEED
    if keys[pygame.K_s]:
        screen_rect_rel_bg.top += SPEED

    screen.fill("purple")

    for point in BackgroundMap.getScreenPoints():
        map_indices = BackgroundMap.getMapOn(Point(screen_rect_rel_bg.left + point.x, screen_rect_rel_bg.top + point.y))
        map_tl_pos_rel_bg = BackgroundMap.getMapTopLeftPointRelativeToMapOrigin(map_indices)
        map_tl_pos_rel_screen = Point(map_tl_pos_rel_bg.x, map_tl_pos_rel_bg.y).getRelativePoint(Point(screen_rect_rel_bg.left, screen_rect_rel_bg.top))
        map_rect = pygame.Rect(map_tl_pos_rel_screen.x,map_tl_pos_rel_screen.y,MAP_WIDTH,MAP_HEIGHT)
        map_color = getMapColor(map_indices[0], map_indices[1])
        pygame.draw.rect(screen,map_color,map_rect)

    pygame.display.flip()
    clock.tick(60)