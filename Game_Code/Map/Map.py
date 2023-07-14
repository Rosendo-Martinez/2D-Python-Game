import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def getRelativePoint(self,point_relative_to):
        return Point(-(point_relative_to.x - self.x), -(point_relative_to.y - self.y))

class Map:
    def __init__(self,map_width,map_height,screen_width,screen_height):
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_topleft = Point(0,0) # relative to map origin, user uses this to move screen around map
        self.important_screen_points_rel_screen_origin = self.getScreenPoints() # list of points to place maps on, relative to screen origin

    def getMapOn(self, point):
        if (point.x == 0):
            i = 1
        elif (point.x > 0):
            i = math.ceil(point.x / self.map_width)
        else:
            i = math.floor(point.x / self.map_width)
        if (point.y == 0):
            j = 1
        elif (point.y > 0):
            j = math.ceil(point.y / self.map_height)
        else:
            j = math.floor(point.y / self.map_height)
        return [i, j]

    def getScreenPoints(self):
        points = []
        p_x = 0
        p_y = 0
        while (p_x <= self.screen_width and p_y <= self.screen_height):
            points.append(Point(p_x,p_y))
            p_x += self.map_width
            if (self.screen_width + self.map_width > p_x and p_x > self.screen_width):
                p_x = self.screen_width
            if (p_x > self.screen_width):
                p_x = 0
                p_y += self.map_height
                if (self.screen_height + self.map_height > p_y and p_y > self.screen_height):
                    p_y = self.screen_height
        return points

    def getMapTopLeftPointRelativeToMapOrigin(self, map_indices):
        # returns the coordinates of the top left point on the given map relative to the map origin
        if (map_indices[0] < 0):
            if (map_indices[1] < 0):
                return Point(map_indices[0] * self.map_width,map_indices[1] * self.map_height)
            else:
                return Point(map_indices[0] * self.map_width,map_indices[1] * self.map_height - self.map_height)
        else:
            if (map_indices[1] < 0):
                return Point(map_indices[0] * self.map_width - self.map_width,map_indices[1] * self.map_height)
            else:
                return Point(map_indices[0] * self.map_width - self.map_width,map_indices[1] * self.map_height - self.map_height)

if __name__ == '__main__':
    myMap = Map(300, 300, 350, 350)
    print('getMapOn Tests')
    print(myMap.getMapOn(Point(2 * myMap.map_width, 3 * myMap.map_height)) == [2, 3])
    print(myMap.getMapOn(Point(1.5 * myMap.map_width, 1 * myMap.map_height)) == [2, 1])
    print(myMap.getMapOn(Point(-7.8 * myMap.map_width, 1 * myMap.map_height)) == [-8, 1])
    print(myMap.getMapOn(Point(-10.1 * myMap.map_width, -12.8 * myMap.map_height)) == [-11, -13])
    print('getRelativePoint Tests')
    print(Point(0, 0).getRelativePoint(Point(7, 10)) == Point(-7, -10))
    print(Point(1, 1).getRelativePoint(Point(3, 2)) == Point(-2, -1))
    print(Point(-7, 8).getRelativePoint(Point(3, 2)) == Point(-10, 6))
    print('getMapTopLeftPointRelativeToMapOrigin Tests')
    print(myMap.getMapTopLeftPointRelativeToMapOrigin([1,1]) == Point(0,0))
    print(myMap.getMapTopLeftPointRelativeToMapOrigin([1,-1]) == Point(0,-myMap.map_height))
    print(myMap.getMapTopLeftPointRelativeToMapOrigin([-1,1]) == Point(-myMap.map_width,0))
    print(myMap.getMapTopLeftPointRelativeToMapOrigin([-1,-1]) == Point(-myMap.map_width,-myMap.map_height))
    map_test_getPoints = Map(50, 50, 100, 100)
    print('getScreenPoints Tests')
    print(map_test_getPoints.getScreenPoints() == [Point(0, 0), Point(50, 0), Point(100, 0), Point(0, 50), Point(50, 50), Point(100, 50), Point(0, 100), Point(50, 100), Point(100, 100)])