import puzzle1

def removeLetters(polymer):
    return set(removeLetter(polymer, letter) for letter in set(polymer.lower()))

def removeLetter(polymer, letter):
    return polymer.replace(letter.lower(), "").replace(letter.upper(), "")

def getAllReactedPolymersRemovingUnit(polymer):
    removedLetterPolymers = removeLetters(polymer)
    return set(puzzle1.reactPolymer(removedLetterPolymer) for removedLetterPolymer in removedLetterPolymers)

def sortPolymersByLen(polymers):
    return sorted(polymers, key=lambda a: len(a))