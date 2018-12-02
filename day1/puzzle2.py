class TimeTravelDevice:
    def __init__(self, inputList):
        frequency = 0
        usedFrequencies = set([frequency])

        duplicateNotFound = True

        while duplicateNotFound:
            for arg in inputList:
                frequency += arg
                if frequency in usedFrequencies:
                    duplicateNotFound = False
                    break
                usedFrequencies.add(frequency)

        self.frequencyLock = frequency
