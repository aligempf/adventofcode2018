import getInput

#inputList = getInput.InputValueReceiver(args=["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]).inputValues
inputList = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/2/input").inputValues

numBoxes = {}

for boxID in inputList:
    boxNumbers = {}
    letters = set(boxID)
    for letter in letters:
        count = boxID.count(letter)
        if not count in numBoxes:
            numBoxes[count] = 0
        if count not in boxNumbers:
            numBoxes[count] += 1
        boxNumbers[count] = True

print(numBoxes[2] * numBoxes[3])