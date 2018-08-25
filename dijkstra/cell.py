#Cell class
class Cell(object):
    def __init__(self, x, y, dist):
        self.x = x
        self.y = y
        self.dist = dist
        self._visited = 0

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value

    #Pretty printing the object
    def __repr__(self):
        return 'Cell(' + repr(self.x) + ', ' + repr(self.y) + ', ' + repr(self.dist) + ', ' + repr(self.visited) + ')'


