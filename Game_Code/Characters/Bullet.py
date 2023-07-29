
import math
import time

from Game_Code.Characters.Direction import Direction


class Bullet:
    def __init__(self, starting_position, direction, speed, dmg, life_time, radius):
        self.direction = direction
        self.speed = speed
        self.dmg = dmg
        self.life_time = life_time
        self.start_time = time.time()
        self.position = starting_position
        self.radius = radius
    def move(self):
        if (self.direction == Direction.N):
            self.position.y += self.speed
        elif (self.direction == Direction.NE):
            self.position.x += self.speed/math.sqrt(2)
            self.position.y += self.speed/math.sqrt(2)
        elif (self.direction == Direction.E):
            self.position.x += self.speed
        elif (self.direction == Direction.SE):
            self.position.x += self.speed/math.sqrt(2)
            self.position.y -= self.speed/math.sqrt(2)
        elif (self.direction == Direction.S):
            self.position.y -= self.speed
        elif (self.direction == Direction.SW):
            self.position.x -= self.speed/math.sqrt(2)
            self.position.y -= self.speed/math.sqrt(2)
        elif (self.direction == Direction.W):
            self.position.x -= self.speed
        elif (self.direction == Direction.NW):
            self.position.x -= self.speed/math.sqrt(2)
            self.position.y += self.speed/math.sqrt(2)
    def collision(self, enemy):
        distance = math.sqrt((self.position.x - enemy.position.x) ** 2 + (self.position.y - enemy.position.y) ** 2)
        return distance < self.radius + enemy.radius
    def attack(self,enemy):
        enemy.health -= self.dmg
    def isDead(self):
        return time.time() > self.start_time + self.life_time

