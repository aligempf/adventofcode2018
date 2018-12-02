def boxCheckSum(inputList):

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

    return numBoxes[2] * numBoxes[3]