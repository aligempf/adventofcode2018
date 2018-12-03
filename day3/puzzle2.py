import puzzle1

def getUniqueSquareID(inputList):
    return getUniqueSquare(inputList)

def getUniqueSquare(inputList):
    inputSquares = set(puzzle1.InputSquare(i) for i in inputList)
    ids = set(i.id for i in inputSquares)
    overlapping = puzzle1.overlappingSquares(inputSquares)
    for square in overlapping:
        if len(overlapping[square]) > 1:
            for id in overlapping[square]:
                if id in ids:
                    ids.remove(id)
    return ids