import math

class Screen:
    def __init__(self, x, y, width, height):
        self._point = Point(x,y)
        self._width = width
        self._height = height
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

def Scroller(screen_width,screen_height,subMap_width,subMap_height):
    screen = Screen(0,0,screen_width,screen_height)
    subMaps = []
    for mappedScreenPoint in _getScreenPointsToTrack(screen_width,screen_height,subMap_width,subMap_height):
        subMaps.append(SubMap(screen,mappedScreenPoint, subMap_height, subMap_width))
    return (screen,subMaps)

def _getScreenPointsToTrack(screen_width,screen_height,subMap_width,subMap_height):
    p_x = 0
    p_y = 0
    while (p_x <= screen_width and p_y <= screen_height):
        yield Point(p_x, p_y)
        p_x += subMap_width
        if (screen_width + subMap_width > p_x and p_x > screen_width):
            p_x = screen_width
        if (p_x > screen_width):
            p_x = 0
            p_y += subMap_height
            if (screen_height + subMap_height > p_y and p_y > screen_height):
                p_y = screen_height


if __name__ == '__main__':
    print('Screen & SubMap Tests')
    myScreen = Screen(0,0,100,100)
    mySubMapMappedToScreenBottomLeft = SubMap(myScreen, Point(0, 100), 50, 50)
    print(mySubMapMappedToScreenBottomLeft.getSubMapData() == ((1,2),Point(0,50)))
    myScreen.moveBy(100,0)
    print(mySubMapMappedToScreenBottomLeft.getSubMapData() == ((2, 2), Point(-50, 50)))
    myScreen.moveTo(-200,-100)
    print(mySubMapMappedToScreenBottomLeft.getSubMapData() == ((-4, 1), Point(0, 100)))