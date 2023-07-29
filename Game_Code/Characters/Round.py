import time

from Game_Code.Characters.AI_Bot import AIBot
from Game_Code.Characters.RandomPoint import RandomPointOnCircleCircumference

class Round:
    def __init__(self,hero, enemy_spawn_radius):
        self.current_round = 0
        self.time_between_rounds = 2
        self.break_time_start = time.time()
        self.enemies = []
        self.hero = hero
        self.enemy_spawn_radius = enemy_spawn_radius
        self.bullets = []
        self.break_on = True
        self.sub_round_interval = 1
        self.last_sub_round_time = None
        self.enemies_spawned = 0
        self.enemy_spawn_rate = 3
        self.sub_round_on = False
        self.enemies_killed = 0
        self.round = 0
    def totalEnemiesToSpawn(self):
        return self.current_round * 9
    def start_sub_round(self):
        if self.last_sub_round_time == None or self.last_sub_round_time + self.sub_round_interval < time.time():
            number_of_enemies_to_spawn = self.enemy_spawn_rate if self.enemy_spawn_rate + self.enemies_spawned <= self.totalEnemiesToSpawn() else self.totalEnemiesToSpawn() - self.enemies_spawned
            self.enemies_spawned += number_of_enemies_to_spawn
            for i in range(number_of_enemies_to_spawn):
                point = RandomPointOnCircleCircumference(self.enemy_spawn_radius, self.hero.position)
                self.enemies.append(AIBot(point.x, point.y, 1.5, radius=30))
            self.last_sub_round_time = time.time()
    def start_round(self):
        self.round += 1
        self.current_round = self.current_round + 1
        self.enemies_spawned = 0
        self.break_on = False
        self.sub_round_on = True
    def remove_dead_enemies(self):
        for enemy in self.enemies:
            if enemy.isDead():
                self.enemies_killed += 1
                self.enemies.remove(enemy)
    def is_round_over(self):
        return self.totalEnemiesToSpawn() == self.enemies_spawned and len(self.enemies) == 0
    def is_round_break_over(self):
        return time.time() > self.break_time_start + self.time_between_rounds
    def start_round_break(self):
        self.break_on = True
        self.sub_round_on = False
        self.break_time_start = time.time()
    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move(self.hero.position)
    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move()
    def bullet_enemy_collision(self):
        for bullet in self.bullets:
            if not bullet.isDead():
                for enemy in self.enemies:
                    if bullet.collision(enemy):
                        bullet.attack(enemy)
                        self.bullets.remove(bullet)
                        break
            else:
                self.bullets.remove(bullet)
    def hero_enemy_collision(self):
        for enemy in self.enemies:
            if enemy.collision(self.hero):
                enemy.attack(self.hero)

    def is_game_over(self):
        return self.hero.isDead()
    def enemy_enemy_collision(self):
        merger = False
        for enemy1 in self.enemies:
            for enemy2 in self.enemies:
                if not enemy1 == enemy2 and enemy1.collision(enemy2):
                    enemy1.merge(enemy2)
                    self.enemies.remove(enemy2)
                    merger = True
                    break
            if merger:
                break
    def reset(self):
        self.current_round = 0
        self.time_between_rounds = 2
        self.break_time_start = time.time()
        self.break_on = True
        self.sub_round_interval = 1
        self.last_sub_round_time = None
        self.enemies_spawned = 0
        self.enemy_spawn_rate = 3
        self.sub_round_on = False
        self.enemies_killed = 0
        self.enemies.clear()
        self.bullets.clear()
        self.round = 0