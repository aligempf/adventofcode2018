def reactPolymer1(polymer):
    while True:
        for i in range(len(polymer)-1):
            if checkLetters((polymer[i],polymer[i+1])):
                polymer = polymer[:i] + polymer[i+2:]
                break

def reactPolymer(polymer):
    while True:
        reaction = singleReaction(polymer)
        if reaction == polymer:
            return polymer
        else:
            polymer = reaction

def singleReaction(polymer):
    shouldReact = []
    for i in range(len(polymer) - 1):
        if i > 0 and shouldReact[i-1]:
            shouldReact.append(False)
            continue
        shouldReact.append(checkLetters(polymer[i:i+2]))
    shouldReact.append(False)
    return doReaction(polymer, shouldReact)

def checkLetters(pair):
    return pair[0].lower() == pair[1].lower() and not pair[0] == pair[1]

def doReaction(polymer, shouldReact):
    reacted = ""
    for index in range(len(shouldReact)):
        if index == 0:
            if not shouldReact[index]:
                reacted += polymer[index]
                continue
        if not shouldReact[index] and not shouldReact[index-1]:
            reacted += polymer[index]
    return reacted
