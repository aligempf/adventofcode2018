import sys
import getInput

inputList = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/1/input", sanitiser=getInput.safeInt).inputValues

frequency = 0

for arg in inputList:
    frequency += arg

print(frequency)
