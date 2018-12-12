class Square:
    def __init__(self, serial):
        self.serial = serial
        self.cells = self.getCells()
        self.areaTable = self.getAreaTable()

    def getCells(self):
        cells = {(x, y): getCellValue(x,y,self.serial) for x in range(1, 301) for y in range(1, 301)}
        return cells

    def getAreaTable(self):
        # Algorithm suggested by /u/PlainSight linking to this: https://en.wikipedia.org/wiki/Summed-area_table
        areaTable = {(x-1,y-1): sum([self.cells[(i,j)] for i in range(1,x+1) for j in range(1,y+1)]) for x in range(1,301) for y in range(1,301) if x == 1 or y == 1}
        for x in range(1, 300):
            for y in range(1, 300):
                areaTable[(x,y)] = sum([self.cells[(x,y)], areaTable[(x-1,y)], areaTable[(x,y-1)], - areaTable[(x-1,y-1)]])
        return areaTable

    def getSmallSquareValue(self, x, y, size):
        value = 0
        for j in range(y, y+size):
            for i in range(x, x+size):
                value += self.cells[(i,j)]
                if value + 4 * ((size - i) * (size - j)) <= self.maxSquareValue:
                    return value
        if value > self.maxSquareValue:
            self.maxSquareValue = value
            self.maxSquareStart = (x, y, size)
        return value

    def getSmallSquareValueFromAreaTable(self, x, y, size):
        return self.areaTable[(x-1,y-1)] + self.areaTable[(x+size-1,y+size-1)] - self.areaTable[(x-1,y+size-1)] - self.areaTable[(x+size-1,y-1)]

    def getMaxSquare(self, size=3):
        return max([(x, y, size, self.getSmallSquareValueFromAreaTable(x,y,size)) for x in range(1,300-size) for y in range(1,300-size)], key=lambda position: position[3])

    def getMaxSquareOfSquares(self):
        return max([self.getMaxSquare(x) for x in range(1,299)], key=lambda square: square[3])

def getCellValue(x, y, serial):
    rackID = 10 + x
    initPowerLevel = rackID * (serial + (rackID * y))
    hundreds = int(str(initPowerLevel)[-3]) if initPowerLevel > 99 else 0
    return hundreds - 5
