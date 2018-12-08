class Step:
    def __init__(self, ID, basetime):
        self.ID = ID
        self.dependencies = set()
        self.done = False

    def __bool__(self):
        return self.done

    def __nonzero__(self):
        return self.__bool__()

    def addDependency(self, dep):
        self.dependencies.add(dep)

    def isReady(self):
        return all(self.dependencies)

    def runStep(self):
        if self or not self.isReady():
            raise Exception
        self.done = True
        return self.done

    def __hash__(self):
        return hash(self.ID)

    def __repr__(self):
        return "Step " + self.ID + " depends on " + ", ".join([dep.ID for dep in self.dependencies])

class Manual:
    def __init__(self, inputList, stepType=Step, baseTime=60):
        steps = {}
        for item in inputList:
            splitList = item.split(' ')
            depID = splitList[1]
            stepID = splitList[7]
            if not depID in steps:
                steps[depID] = stepType(depID, baseTime)
            if not stepID in steps:
                steps[stepID] = stepType(stepID, baseTime)

            steps[stepID].addDependency(steps[depID])

        self.steps = set(steps.values())
        self.stepOrder = ""
        self.nextStep = self.getNextStep()

    def getReadySteps(self):
        return set(filter(lambda step: not step, filter(lambda step: step.isReady(), self.steps)))

    def getNextStep(self):
        return min(self.getReadySteps(), key=lambda step: step.ID)

    def runStep(self):
        self.nextStep = self.getNextStep()
        self.stepOrder += self.nextStep.ID
        self.nextStep.runStep()

    def __repr__(self):
        return self.stepOrder

    def runAllSteps(self):
        while not all(self.steps):
            self.runStep()
