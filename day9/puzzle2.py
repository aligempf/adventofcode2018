import puzzle1

class BigCircle(puzzle1.Circle):
    def __init__(self, numPlayers, maxMarbleValue):
        puzzle1.Circle.__init__(self, numPlayers, maxMarbleValue*100)
