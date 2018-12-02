import sys

inputList = []

with open("input.txt") as fin:
    inputList = fin.read().split('\n')

frequency = 0
usedFrequencies = set([frequency])

duplicateNotFound = True

while duplicateNotFound:
    for arg in inputList:
        frequency += int(arg)
        if frequency in usedFrequencies:
            duplicateNotFound = False
            break
        usedFrequencies.add(frequency)

print(frequency)
