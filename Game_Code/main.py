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

MAP_WIDTH = 150
MAP_HEIGHT = 150
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SPEED = 5

MAPS = ['black','white']

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen_rect, subMaps = Scroller(SCREEN_WIDTH,SCREEN_HEIGHT,MAP_WIDTH,MAP_HEIGHT)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        screen_rect.moveBy(-SPEED,0)
    if keys[pygame.K_d]:
        screen_rect.moveBy(SPEED,0)
    if keys[pygame.K_w]:
        screen_rect.moveBy(0,-SPEED)
    if keys[pygame.K_s]:
        screen_rect.moveBy(0,SPEED)

    screen.fill("purple")
    for subMap in subMaps:
        subMapIndices, subMapTopLeftRelativeToScreenTopLeft = subMap.getSubMapData()
        subMapColor = getMapColor(*subMapIndices)
        pygame.draw.rect(screen,subMapColor, pygame.Rect(subMapTopLeftRelativeToScreenTopLeft.x,subMapTopLeftRelativeToScreenTopLeft.y,MAP_WIDTH,MAP_HEIGHT))

    pygame.display.flip()
    clock.tick(60)