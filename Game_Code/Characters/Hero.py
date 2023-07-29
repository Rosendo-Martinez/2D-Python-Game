from Game_Code.BackgroundScroller.BackgroundScroller import Point
import math
from Game_Code.Characters.Bullet import Bullet
from Game_Code.Characters.Direction import Direction
import time


class Hero:
    def __init__(self, x, y, speed, starting_health=20, gun_recharge_time = 0.1, radius = 10):
        self.position = Point(x,y)
        self.speed = speed
        self.health = starting_health
        self.gun_recharge_time = gun_recharge_time
        self.last_time_gun_shot = None
        self.radius = radius
        self.facingDirection = Direction.E
    def move(self, dir):
        self.facingDirection = dir
        if (dir == Direction.N):
            self.position.y += self.speed
        elif (dir == Direction.NE):
            self.position.x += self.speed/math.sqrt(2)
            self.position.y += self.speed/math.sqrt(2)
        elif (dir == Direction.E):
            self.position.x += self.speed
        elif (dir == Direction.SE):
            self.position.x += self.speed/math.sqrt(2)
            self.position.y -= self.speed/math.sqrt(2)
        elif (dir == Direction.S):
            self.position.y -= self.speed
        elif (dir == Direction.SW):
            self.position.x -= self.speed/math.sqrt(2)
            self.position.y -= self.speed/math.sqrt(2)
        elif (dir == Direction.W):
            self.position.x -= self.speed
        elif (dir == Direction.NW):
            self.position.x -= self.speed/math.sqrt(2)
            self.position.y += self.speed/math.sqrt(2)
    def changeFacingDirecrtion(self,dir):
        self.facingDirection = dir
    def isDead(self):
        return self.health <= 0
    def shoot(self):
        if self.last_time_gun_shot == None or time.time() > self.last_time_gun_shot + self.gun_recharge_time:
            self.last_time_gun_shot = time.time()
            return Bullet(Point(self.position.x, self.position.y),
                          self.facingDirection,
                          speed=5,
                          dmg=20,
                          life_time=10,
                          radius=4)
        return None

    def reset(self, x, y, speed, starting_health = 20):
        self.position = Point(x,y)
        self.health = starting_health
        self.speed = speed
        self.last_time_gun_shot = None
        self.facingDirection = Direction.E