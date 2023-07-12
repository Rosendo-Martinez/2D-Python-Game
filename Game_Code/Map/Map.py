import math

def getRelativePoint(p1, p2):
    # returns p1 relative to p2
    return {'x':-(p2['x'] - p1['x']), 'y':-(p2['y'] - p1['y'])}


class Map:
    def __init__(self,map_width,map_height,screen_width,screen_height):
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def getMapOn(self, x, y):
        if (x == 0):
            i = 1
        elif (x > 0):
            i = math.ceil(x / self.map_width)
        else:
            i = math.floor(x / self.map_width)
        if (y == 0):
            j = 1
        elif (y > 0):
            j = math.ceil(y / self.map_height)
        else:
            j = math.floor(y / self.map_height)
        return [i, j]

    def getImportantPointsOnScreen(self):
        points = []
        p_x = 0
        p_y = 0
        while (p_x <= self.screen_width and p_y <= self.screen_height):
            points.append({'x':p_x,'y':p_y})
            p_x += self.map_width
            if (self.screen_width + self.map_width > p_x and p_x > self.screen_width):
                p_x = self.screen_width
            if (p_x > self.screen_width):
                p_x = 0
                p_y += self.map_height
                if (self.screen_height + self.map_height > p_y and p_y > self.screen_height):
                    p_y = self.screen_height
        return points

    def getMapTopLeftPosRelToBg(self,indicies):
        # case 1: -x -y
        # case 2: -x y
        # case 3: x -y
        # case 4: x y
        if (indicies[0] < 0):
            if (indicies[1] < 0):
                return {'x': indicies[0] * self.map_width,
                        'y': indicies[1] * self.map_height}
            else:
                return {'x':indicies[0]*self.map_width,
                        'y':indicies[1]*self.map_height-self.map_height}
        else:
            if (indicies[1] < 0):
                return {'x': indicies[0] * self.map_width-self.map_width,
                        'y': indicies[1] * self.map_height}
            else:
                return {'x': indicies[0] * self.map_width-self.map_width,
                        'y': indicies[1] * self.map_height-self.map_height}

if __name__ == '__main__':
    print('getMapOn() tests')
    myMap = Map(300,300,350,350)
    print(myMap.getMapOn(2 * myMap.map_width, 3 * myMap.map_height) == [2,3])
    print(myMap.getMapOn(1.5 * myMap.map_width, 1 * myMap.map_height) == [2,1])
    print(myMap.getMapOn(-7.8 * myMap.map_width, 1 * myMap.map_height) == [-8,1])
    print(myMap.getMapOn(-10.1 * myMap.map_width, -12.8 * myMap.map_height) == [-11,-13])
    print('getRelativePoint test')
    print(getRelativePoint({'x':0,'y':0},{'x':7,'y':10}) == {'x':-7,'y':-10})
    print(getRelativePoint({'x': 1, 'y': 1}, {'x': 3, 'y': 2}) == {'x':-2,'y':-1})
    print(getRelativePoint({'x': -7, 'y': 8}, {'x': 3, 'y': 2}) == {'x':-10,'y':6})