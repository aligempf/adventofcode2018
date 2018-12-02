class TimeTravelDevice:
    def __init__(self, inputList):
        frequency = 0

        for arg in inputList:
            frequency += arg

        self.frequency = frequency
