def commonBoxLetters(inputList):
    for boxIndex in range(len(inputList)):
        boxID = inputList[boxIndex]
        for compBoxIndex in range(boxIndex+1,len(inputList)):
            compBoxID = inputList[compBoxIndex]
            numDiffs = 0
            for letterIndex in range(min(len(boxID), len(compBoxID))):
                if not compBoxID[letterIndex] == boxID[letterIndex]:
                    numDiffs += 1
                if numDiffs > 1:
                    break
            if numDiffs == 1:
                break
        if numDiffs == 1:
            break

    letters = [boxID[letterIndex] for letterIndex in range(len(boxID)) if boxID[letterIndex] == compBoxID[letterIndex]]
    return "".join(letters)
