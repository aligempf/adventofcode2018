import puzzle1

def figureOutCodes(possibleFunctions):
    singleFunctions = getSingleFunctions(possibleFunctions)
    possibleFunctions = pullOutConfirmed(possibleFunctions, singleFunctions)
    return possibleFunctions

def getSingleFunctions(possibleFunctions):
    return {code: list(possibleFunctions[code])[0] for code in possibleFunctions if len(possibleFunctions[code]) == 1}

def pullOutConfirmed(possibleFunctions, confirmedFunctions):
    for code in possibleFunctions:
        for confirmedFunction in confirmedFunctions.values():
            if confirmedFunction in possibleFunctions[code]:
                if code in confirmedFunctions:
                    if not confirmedFunctions[code] == confirmedFunction:
                        possibleFunctions[code].remove(confirmedFunction)
                else:
                    possibleFunctions[code].remove(confirmedFunction)
    return possibleFunctions

class KnownCPU(puzzle1.CPU):
    def __init__(self, functionDefinitions):
        self.functionDefinitions = functionDefinitions
        puzzle1.CPU.__init__(self)

    def __call__(self, code):
        self.functionDefinitions[code[0]](code, self)

class Code:
    def __init__(self, code):
        self.code = code

    def __getitem__(self, item):
        return self.code[item]

    def __repr__(self):
        return str(self.code)

def parseInput(inputList):
    return [Code(map(int, inputList[index].split(" "))) for index in range(len(inputList)) if not "Before" in inputList[index-1] and len(inputList[index].split(" ")) == 4]
