class Square:
    def __init__(self, serial):
        self.serial = serial
        self.cells = self.getCells()
        self.maxSquareValue = 0
        self.maxSquareStart = (0, 0, 0)

    def getCells(self):
        cells = {(x, y): getCellValue(x,y,self.serial) for x in range(1, 301) for y in range(1, 301)}
        return cells

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

    def getMaxSquare(self, size=3):
        return max([(x, y, size) for x in range(1,302-size) for y in range(1,302-size)], key=lambda position: self.getSmallSquareValue(position[0], position[1], position[2]))

def getCellValue(x, y, serial):
    rackID = 10 + x
    initPowerLevel = rackID * (serial + (rackID * y))
    hundreds = int(str(initPowerLevel)[-3]) if initPowerLevel > 99 else 0
    return hundreds - 5
