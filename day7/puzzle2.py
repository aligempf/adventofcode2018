import puzzle1

class ConcurrentStep(puzzle1.Step):
    def __init__(self, ID, baseTime):
        self.timeTaken = baseTime + ord(ID) - 64
        self.timeLeft = self.timeTaken
        self.running = False
        puzzle1.Step.__init__(self, ID, baseTime)

    def addTime(self, time):
        self.timeLeft -= time
        if self.timeLeft <= 0:
            self.done = True
            self.running = False

    def runStep(self):
        if self or not self.isReady():
            raise Exception(self, self.running, puzzle1.Step.isReady(self))
        self.running = True

    def isReady(self):
        return not self.running and puzzle1.Step.isReady(self)


class CollabarativeManual(puzzle1.Manual):
    def __init__(self, inputList, numWorkers, baseTime=60):
        self.time = 0
        self.numWorkers = numWorkers
        puzzle1.Manual.__init__(self, inputList, stepType=ConcurrentStep, baseTime=baseTime)

    def getNextInterestingTime(self):
        return min(filter(lambda step: not step, self.getRunningSteps()), key=lambda step: step.timeLeft).timeLeft

    def addTime(self, time):
        self.time += time
        for step in self.getRunningSteps():
            step.addTime(time)

    def getNextSteps(self):
        readySteps = self.getReadySteps()
        allReadyOrRunningStepsInOrder = sorted(self.getRunningSteps(), key=lambda step: step.ID) + sorted(readySteps, key=lambda step: step.ID)
        return allReadyOrRunningStepsInOrder[0:min(self.numWorkers, len(allReadyOrRunningStepsInOrder))]

    def startRunningSteps(self, steps):
        for step in steps:
            if not step.running: step.runStep()

    def getRunningSteps(self):
        return set(filter(lambda step: not step, filter(lambda step: step.running, self.steps)))

    def runAllSteps(self):
        while not all(self.steps):
            nextSteps = self.getNextSteps()
            for step in nextSteps:
                if not step.running: self.stepOrder += step.ID
            self.startRunningSteps(nextSteps)
            self.addTime(self.getNextInterestingTime())
