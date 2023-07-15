import math

class Screen:
    def __init__(self, x, y, width, height):
        self._point = Point(x,y)
        self._width = width
        self._height = height
        self._mappedSubMaps = None
    def moveBy(self,x,y):
        self._point.x += x
        self._point.y += y
    def moveTo(self,x,y):
        self._point.x = x
        self._point.y = y

class SubMap:
    def __init__(self, screen, mappedScreenPointRelativeToScreenOrigin, height, width):
        self._screen = screen
        self._mappedScreenPointRelativeToScreenOrigin = mappedScreenPointRelativeToScreenOrigin
        self._height = height
        self._width = width
    def getSubMapData(self):
        # returns a tuple (i,j,Point)
        indices = self._getIndicies(self._getMappedScreenPointRelativeMapOrigin())
        subMapTopLeftRelativeToScreenTopLeft = self._getSubMapTopLeftRelativeToScreenTopLeft(indices[0],indices[1])
        return (indices,subMapTopLeftRelativeToScreenTopLeft)
    def _getMappedScreenPointRelativeMapOrigin(self):
        return self._screen._point + self._mappedScreenPointRelativeToScreenOrigin
    def _getSubMapTopLeftRelativeToScreenTopLeft(self,i,j):
        return self._getSubMapTopLeft(i,j).getRelativePoint(self._screen._point)
    def _getSubMapTopLeft(self,i,j):
        # returns the coordinates of the top left point on the given map relative to the map origin
        if (i < 0):
            if (j < 0):
                return Point(i * self._width, j * self._height)
            else:
                return Point(i * self._width, j * self._height - self._height)
        else:
            if (j < 0):
                return Point(i * self._width - self._width, j * self._height)
            else:
                return Point(i * self._width - self._width,
                             j * self._height - self._height)
    def _getIndicies(self, point):
        if (point.x == 0):
            i = 1
        elif (point.x > 0):
            i = math.ceil(point.x / self._width)
        else:
            i = math.floor(point.x / self._width)
        if (point.y == 0):
            j = 1
        elif (point.y > 0):
            j = math.ceil(point.y / self._height)
        else:
            j = math.floor(point.y / self._height)
        return (i,j)

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def getRelativePoint(self,point_relative_to):
        return Point(-(point_relative_to.x - self.x), -(point_relative_to.y - self.y))
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def __str__(self):
        return f'Point(x={self.x},y={self.y})'

class Map:
    def __init__(self,map_width,map_height,screen_width,screen_height):
        self.map_width = map_width
        self.map_height = map_height
        self.screen = Screen(0,0,screen_width,screen_height)
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
        while (p_x <= self.screen._width and p_y <= self.screen._height):
            points.append(Point(p_x,p_y))
            p_x += self.map_width
            if (self.screen._width + self.map_width > p_x and p_x > self.screen._width):
                p_x = self.screen._width
            if (p_x > self.screen._width):
                p_x = 0
                p_y += self.map_height
                if (self.screen._height + self.map_height > p_y and p_y > self.screen._height):
                    p_y = self.screen._height
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

    #SubMap Tests
    print('Screen & SubMap Tests')
    myScreen = Screen(0,0,100,100)
    mySubMap = SubMap(myScreen,Point(0,100),50,50)
    myScreen.moveBy(100,0)
    print(mySubMap.getSubMapData() == ((2,2),Point(-50,50)))
    myScreen.moveTo(-200,-100)
    print(mySubMap.getSubMapData() == ((-4, 1), Point(0,100)))