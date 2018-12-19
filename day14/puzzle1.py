class Scoreboard:
    def __init__(self, startingScores, numElves=2):
        self.scores = startingScores
        self.elves = set(Elf(i) for i in range(numElves))

    def __repr__(self):
        #return str(self.scores) + "\n" + str(self.elves)
        if len(self.scores) < 10:
            return str(self.scores) + "\n" + str(self.elves)
        else:
            return "".join(map(str, self.scores[-10:]))

    def tasteTest(self):
        sumOfRecipes = sum([self.scores[i.index] for i in self.elves])
        self.scores += map(int, list(str(sumOfRecipes)))
        for elf in self.elves:
            elf.index = (1 + elf.index + self.scores[elf.index]) % len(self.scores)
        return sumOfRecipes

    def numBeforeLast10(self):
        if len(self.scores) < 10:
            return 0
        else:
            return len(self.scores) - 10

    def getTenScoresAfter(self, index):
        return self.scores[index:index + 10]

class Elf:
    def __init__(self, startingIndex):
        self.index = startingIndex

    def __iadd__(self, other):
        self.index += other
        return self

    def __repr__(self):
        return "Elf at index %i" %self.index
