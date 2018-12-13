class Pots:
    def __init__(self, inputList):
        pots = inputList[0].split(" ")[2]
        self.state = {i for i in range(0, len(pots)) if pots[i] == "#"}
        self.rules = set(Rule(rule) for rule in inputList[1:])
        self.centerPot = 0
        self.startFalses = max(self.rules, key=lambda rule: rule.startFalses).startFalses
        self.endFalses = max(self.rules, key=lambda rule: rule.endFalses).endFalses
        self.time = 0
        self.prevStates = {}
        self.repeating = False

    def getBoundaryIndices(self):
        return (min(self.state) - self.startFalses, max(self.state) + self.endFalses)

    def doGeneration(self):
        boundary = self.getBoundaryIndices()
        newState = set()
        for x in range(boundary[0], boundary[1] + 1):
            plant = self.checkAllRules(self.getStateFromPot(x))
            if plant:
                newState.add(x)

        self.prevStates[self.normaliseState(self.state)] = self.time

        if self.normaliseState(newState) in self.prevStates:
            self.repeating = True
        self.time += 1
        self.state = newState

    def normaliseState(self, state):
        minInState = min(state)
        return frozenset(pot - minInState for pot in state)

    def checkAllRules(self, state):
        return any(map(lambda rule: rule.checkRule(state), self.rules))

    def __repr__(self):
        boundary = self.getBoundaryIndices()
        strRep = ""
        for x in range(boundary[0], boundary[1] + 1):
            strRep += "#" if x in self.state else "."
        return strRep

    def getStateFromPot(self, pot):
        localState = []
        for i in range(pot-2, pot+3):
            localState.append(True) if i in self.state else localState.append(False)
        return localState

    def getGenerationSum(self):
        return sum(self.state)

class Rule:
    def __init__(self, rule):
        splitRule = rule.split(" => ")
        self.state = map(lambda position: position == "#",splitRule[0])
        self.result = splitRule[1] == "#"
        if self.result:
            self.startFalses = self.state.index(True)
            self.endFalses = list(reversed(self.state)).index(True)
        else:
            self.startFalses = 0
            self.endFalses = 0

    def __repr__(self):
        return str(self.state) + " => " + str(self.result)

    def checkRule(self, state):
        if state == self.state:
            return self.result
