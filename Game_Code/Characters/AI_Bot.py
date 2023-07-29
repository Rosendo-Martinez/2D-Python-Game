from Game_Code.BackgroundScroller.BackgroundScroller import Point
import math
import time

class AIBot:
    def __init__(self, x, y,speed, attack_cooldown_time = 3, dmg=5, radius=10, health = 50):
        self.position = Point(x,y)
        self.speed = speed
        self.dmg = dmg
        self.radius = radius
        self.attack_cooldown_time = attack_cooldown_time
        self.time_of_last_attack = None
        self.health = health
    def move(self, point):
        rel_dir = point - self.position
        mag = math.sqrt((rel_dir.x**2) + (rel_dir.y**2))
        unit_rel_dir = Point(rel_dir.x/mag,rel_dir.y/mag)
        velocity_vec = Point(unit_rel_dir.x*self.speed,unit_rel_dir.y*self.speed)
        self.position.x += velocity_vec.x
        self.position.y += velocity_vec.y
    def collision(self, other):
        distance = math.sqrt((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2)
        return distance < self.radius + other.radius
    def attack(self,other):
        if self.canAttack():
            other.health -= self.dmg
            if other.health < 0:
                other.health = 0
            self.time_of_last_attack = time.time()
            return True
        return False
    def canAttack(self):
        if self.time_of_last_attack == None or time.time() > self.attack_cooldown_time + self.time_of_last_attack:
            return True
        return False
    def isDead(self):
        return self.health <= 0
    def merge(self,other):
        if (self.radius > other.radius):
            self.radius = self.radius + other.radius/5
        else:
            self.radius = other.radius + self.radius/5
            self.position.x = other.position.x
            self.position.y = other.position.y
        if (self.health > other.health):
            self.health = self.health + other.health/7
        else:
            self.health = self.health/7 + other.health
        if (self.speed > other.speed):
            self.speed = self.speed + other.speed/40
        else:
            self.speed = self.speed/40 + other.speed
        self.dmg += 1