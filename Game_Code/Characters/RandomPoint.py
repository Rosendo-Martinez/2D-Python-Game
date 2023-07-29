import math
import random
from Game_Code.BackgroundScroller.BackgroundScroller import Point


def RandomPointOnCircleCircumference(inner_radius, point, max_distance=25):
    random_radian = 2 * 3.14 * random.random()
    random_distance = max_distance * random.random()
    ajdLength = math.cos(random_radian) * (inner_radius + random_distance)
    opstLength = math.sin(random_radian) * (inner_radius + random_distance)
    return Point(ajdLength + point.x, opstLength + point.y)