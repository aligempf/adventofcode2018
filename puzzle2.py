import sys
import getInput

inputList = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/1/input",sanitiser=getInput.safeInt).inputValues

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

print(frequency)
