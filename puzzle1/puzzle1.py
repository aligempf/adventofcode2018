import sys

inputList = []

with open("input.txt") as fin:
    inputList = fin.read().split('\n')

frequency = 0

for arg in inputList:
    frequency += int(arg)

print(frequency)