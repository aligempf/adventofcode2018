from collections import deque
# Deque is SIGNIFICANTLY faster than a normal list ... who knew?

def parseInput(inputList):
    splitInput = inputList.split(" ")
    return map(int, (splitInput[0], splitInput[6]))

class Circle:
    def __init__(self, numPlayers, maxMarbleValue):
        self.numPlayers = numPlayers
        self.maxMarbleValue = maxMarbleValue
        self.circle = deque([0])
        self.players = {id: Elf(id) for id in range(self.numPlayers)}
        self.lowestAvailableMarble = 1

    def __getitem__(self, item):
        return self.circle[item]

    def addMarble(self):

        if self.lowestAvailableMarble % 23 == 0:
            self.circle.rotate(-7)
            extra = self.circle.popleft()
            self.circle.rotate(1)
            self.lowestAvailableMarble += 1
            return self.lowestAvailableMarble - 1 + extra
        else:
            self.circle.rotate(1)
            self.circle.appendleft(self.lowestAvailableMarble)
            self.lowestAvailableMarble += 1
            return 0

    def playGame(self):
        for marble in range(1, self.maxMarbleValue + 1):
            self.players[marble % self.numPlayers].takeTurn(self)

    def sortPlayersByScore(self, reverse=True):
        return sorted(self.players, key=lambda player: self.players[player].score, reverse=reverse)

    def getHighestScorePlayer(self):
        return self.players[self.sortPlayersByScore()[0]]

class Elf:
    def __init__(self, id):
        self.id = id
        self.score = 0

    def __repr__(self):
        return "Elf %i with score %i" %(self.id, self.score)

    def __hash__(self):
        return hash(self.id)

    def takeTurn(self, circle):
        self.score += circle.addMarble()
