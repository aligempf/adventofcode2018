def numOverlappingSquares(inputList):
    inputSquares = set(InputSquare(i) for i in inputList)
    allSquaresIDs = overlappingSquares(inputSquares)
    return len(getOverlapping(allSquaresIDs))

def overlappingSquares(inputSquares):
    idSquareDict = {i.id: i.getSquares() for i in inputSquares}
    overlapping = {}
    for id in idSquareDict:
        overlaps = False
        for square in idSquareDict[id]:
            if square in overlapping and not id in overlapping[square]:
                overlapping[square].add(id)
            elif square not in overlapping:
                overlapping[square] = set([id])
            elif id in overlapping[square]:
                raise Exception
    return overlapping

class InputSquare:
    def __init__(self, inputString):
        self.values = tuple(inputString.split(" "))
        self.id = int(self.values[0].strip('#'))
        self.topLeft = tuple(map(int, self.values[2].strip(":").split(",")))
        self.sides = tuple(map(int, self.values[3].split("x")))

    def getSquares(self):
        return set((self.topLeft[0]+i,self.topLeft[1]+j) for i in range(self.sides[0]) for j in range(self.sides[1]))

    def printSquare(self):
        square = self.getSquares()
        for x in range(self.topLeft[0]+self.sides[0]):
            for y in range(self.topLeft[1] + self.sides[1]):
                if (x, y) in square:
                    print("#"),
                else:
                    print("."),
            print("\n")

def getOverlapping(overlapping):
    return set(square for square in overlapping if len(overlapping[square]) > 1)
