import time
import pygame
from Game_Code.BackgroundScroller.BackgroundScroller import *
from Game_Code.Characters.Hero import Hero, Direction
from Game_Code.Characters.AI_Bot import AIBot
from Game_Code.Characters.Round import Round
from Game_Code.Leaderboard.Leaderboard import LeaderBoard
import os


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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SPEED = 5

MAPS = ['black','white']

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen_rect, subMaps = Scroller(SCREEN_WIDTH,SCREEN_HEIGHT,MAP_WIDTH,MAP_HEIGHT)
clock = pygame.time.Clock()

fontSmall = pygame.font.Font('freesansbold.ttf', 20)
fontMedium = pygame.font.Font('freesansbold.ttf', 30)
fontLarge = pygame.font.Font('freesansbold.ttf', 60)

hero_pos_rel_screen_tl = Point(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
hero = Hero(hero_pos_rel_screen_tl.x,hero_pos_rel_screen_tl.y,3, radius=15)
round = Round(hero,500)
game_time_rect = pygame.Rect(10,10,0,0)
kill_count_rect = pygame.Rect(80,10,0,0)

aiBots = round.enemies
bullets = round.bullets

leaderboard = LeaderBoard(os.path.join('.','Leaderboard','leaderboard.csv'))
leaderboard_data = None

current_game_start_time = pygame.time.get_ticks()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    if not hero.isDead():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and keys[pygame.K_d]:
            hero.move(Direction.SE)
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            hero.move(Direction.NE)
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            hero.move(Direction.NW)
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            hero.move(Direction.SW)
        elif keys[pygame.K_a]:
            hero.move(Direction.W)
        elif keys[pygame.K_d]:
            hero.move(Direction.E)
        elif keys[pygame.K_w]:
            hero.move(Direction.S)
        elif keys[pygame.K_s]:
            hero.move(Direction.N)
        if keys[pygame.K_SPACE]:
            bullet = hero.shoot()
            if bullet != None:
                bullets.append(bullet)

        if round.break_on and round.is_round_break_over():
            round.start_round()
        elif round.sub_round_on and not round.is_round_over():
            round.start_sub_round()
        elif round.sub_round_on and round.is_round_over():
            round.start_round_break()

        screen_tl_rel_bg = hero.position - hero_pos_rel_screen_tl
        screen_rect.moveTo(screen_tl_rel_bg.x, screen_tl_rel_bg.y)
        round.remove_dead_enemies()
        round.move_enemies()
        round.move_bullets()
        round.bullet_enemy_collision()
        round.hero_enemy_collision()
        round.enemy_enemy_collision()

        screen.fill("purple")
        for subMap in subMaps:
            subMapIndices, subMapTopLeftRelativeToScreenTopLeft = subMap.getSubMapData()
            subMapColor = getMapColor(*subMapIndices)
            pygame.draw.rect(screen,subMapColor, pygame.Rect(subMapTopLeftRelativeToScreenTopLeft.x,subMapTopLeftRelativeToScreenTopLeft.y,MAP_WIDTH,MAP_HEIGHT))
        for bullet in bullets:
            bullet_rel_screen = bullet.position.getRelativePoint(screen_tl_rel_bg)
            pygame.draw.circle(screen,'yellow',(bullet_rel_screen.x,bullet_rel_screen.y),bullet.radius)
        pygame.draw.circle(screen,'red',(hero_pos_rel_screen_tl.x,hero_pos_rel_screen_tl.y),hero.radius)
        for enemy in aiBots:
            aibot_rel_player_pos = enemy.position.getRelativePoint(screen_tl_rel_bg)
            pygame.draw.circle(screen,'green', (aibot_rel_player_pos.x,aibot_rel_player_pos.y), enemy.radius)

        ticks = pygame.time.get_ticks() - current_game_start_time
        seconds = int(ticks/1000 % 60)
        minutes = int(ticks/(1000 * 60))
        formatted_time_string = f'{minutes:02d}:{seconds:02d}'
        formatted_kill_count_string = f'Score: {round.enemies_killed:04d}'
        time_text = fontSmall.render(formatted_time_string, True, 'white', 'black')
        kill_count_text = fontSmall.render(formatted_kill_count_string, True, 'white', 'black')
        hero_health_string = f'Health: {hero.health:02d}'
        hero_health_text = fontSmall.render(hero_health_string, True, 'white', 'black')
        hero_health_text_rect = hero_health_text.get_rect()
        hero_health_text_rect.topleft = (10, 70)
        screen.blit(time_text,game_time_rect)
        screen.blit(kill_count_text,kill_count_rect)
        screen.blit(hero_health_text,hero_health_text_rect)
        round_text = fontSmall.render(f'Round: {round.round:02d}',True,'white','black')
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (10,40)
        screen.blit(round_text,round_text_rect)

        if hero.isDead():
            leaderboard.save(round.round,ticks,round.enemies_killed)
            leaderboard_data = leaderboard.get_rows()

    else:
        screen.fill('tan')
        game_over_string = 'Game Over'
        game_over_text = fontLarge.render(game_over_string, True, 'Blue')
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (SCREEN_WIDTH/2,50)
        screen.blit(game_over_text,game_over_text_rect)

        restart_text = fontMedium.render('Retry', True, 'red')
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT - 90)
        pygame.draw.circle(screen,(189,218,87),restart_text_rect.center,restart_text_rect.width/2 + 10)
        screen.blit(restart_text,restart_text_rect)

        leaderboard_header_text = fontMedium.render('Leaderboard',True,'Red')
        leaderboard_header_text_rect = leaderboard_header_text.get_rect()
        leaderboard_header_text_rect.center = (SCREEN_WIDTH/2,110)
        screen.blit(leaderboard_header_text,leaderboard_header_text_rect)
        leaderboard_titles_formatted = '{:<10} {:<15} {:<9}'.format('Round','Time','Score')
        leaderboard_titles_text = fontMedium.render(leaderboard_titles_formatted,True,'Green')
        leaderboard_titles_text_rect = leaderboard_titles_text.get_rect()
        leaderboard_titles_text_rect.center = (SCREEN_WIDTH/2,150)
        screen.blit(leaderboard_titles_text,leaderboard_titles_text_rect)

        current_height = 190
        for i in range(1, len(leaderboard_data)):
            seconds = int(int(leaderboard_data[i][1]) / 1000 % 60)
            minutes = int(int(leaderboard_data[i][1]) / (1000 * 60))
            formatted_time_string = f'{minutes:02d}:{seconds:02d}'
            if (leaderboard.index_of_last_replaced_row == i):
                leaderboard_score_text = fontSmall.render(
                    f'{leaderboard_data[i][0]:<10} {formatted_time_string:<13} {leaderboard_data[i][2]:>13}', True,
                    'Black', 'silver')
            else:
                leaderboard_score_text = fontSmall.render(
                    f'{leaderboard_data[i][0]:<10} {formatted_time_string:<13} {leaderboard_data[i][2]:>13}', True,
                    'Black')
            leaderboard_score_text_rect = leaderboard_score_text.get_rect()
            leaderboard_score_text_rect.center = (SCREEN_WIDTH/2, current_height)
            current_height += 40
            screen.blit(leaderboard_score_text,leaderboard_score_text_rect)

        if leaderboard.index_of_last_replaced_row != None:
            end_message_text = fontMedium.render('Way too go, new high score!', True, (255,0,127))
        else:
            end_message_text = fontMedium.render('Nice try, but no new high score.', True, (200,0,127))
        end_message_text_rect = end_message_text.get_rect()
        end_message_text_rect.center = (SCREEN_WIDTH / 2, current_height + 50)
        screen.blit(end_message_text,end_message_text_rect)

        if pygame.mouse.get_pressed()[0]:
            if restart_text_rect.collidepoint(pygame.mouse.get_pos()):
                screen_rect.restart()
                round.reset()
                hero.reset(hero_pos_rel_screen_tl.x,hero_pos_rel_screen_tl.y,3)
                current_game_start_time = pygame.time.get_ticks()


    pygame.display.flip()
    clock.tick(65)