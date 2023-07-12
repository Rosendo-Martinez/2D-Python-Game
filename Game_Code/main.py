import pygame
from Game_Code.Map.Map import *

def getMapColor(m,n):
    # M even,odd is black
    # M even,even is white
    # M odd,even is black
    # M odd,odd white
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

'''
Breaks with this params:
MAP_WIDTH = 30
MAP_HEIGHT = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
'''

MAP_WIDTH = 30
MAP_HEIGHT = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BackgroundMap = Map(MAP_WIDTH,MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
SPEED = 3

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

    #screen_rect_rel_bg.left += 200
    screen.fill("purple")
    for point in BackgroundMap.getImportantPointsOnScreen():
        map_indicies = BackgroundMap.getMapOn(screen_rect_rel_bg.left + point['x'],screen_rect_rel_bg.top + point['y'])
        map_tl_pos_rel_bg = BackgroundMap.getMapTopLeftPosRelToBg(map_indicies)
        map_tl_pos_rel_screen = getRelativePoint(map_tl_pos_rel_bg,{'x':screen_rect_rel_bg.left,'y':screen_rect_rel_bg.top})
        map_rect = pygame.Rect(map_tl_pos_rel_screen['x'],map_tl_pos_rel_screen['y'],MAP_WIDTH,MAP_HEIGHT)
        map_color = getMapColor(map_indicies[0],map_indicies[1])
        pygame.draw.rect(screen,map_color,map_rect)

    pygame.display.flip()
    clock.tick(60)