import day1.puzzle1
import day1.puzzle2
import day2.puzzle1
import day2.puzzle2
import day3.puzzle1
import day3.puzzle2
import day4.puzzle1
import day4.puzzle2
import day5.puzzle1
import day5.puzzle2
import day6.puzzle1
import day7.puzzle1
import day7.puzzle2
import day8.puzzle1
import day9.puzzle1
import day9.puzzle2
import day10.puzzle1
import day11.puzzle1
import getInput
import sys

if "all" in sys.argv:
    args = map(str, list(range(1,26)))
else:
    args = sys.argv
    
if "1" in args:
    inputList1 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/1/input", sanitiser=getInput.safeInt).inputValues

    device1 = day1.puzzle1.TimeTravelDevice(inputList1)
    print(device1.frequency)

    device2 = day1.puzzle2.TimeTravelDevice(inputList1)
    print(device2.frequencyLock)

if "2" in args:
    inputList2 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/2/input", sanitiser=getInput.safeString).inputValues

    boxCheckSum = day2.puzzle1.boxCheckSum(inputList2)
    print(boxCheckSum)

    commonBoxLetters = day2.puzzle2.commonBoxLetters(inputList2)
    print(commonBoxLetters)

if "3" in args:
    inputList3 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/3/input", sanitiser=getInput.safeString).inputValues
    
    numOverlappingSquares = day3.puzzle1.numOverlappingSquares(inputList3)
    print(numOverlappingSquares)

    uniqueSquareID = day3.puzzle2.getUniqueSquareID(inputList3)
    print(uniqueSquareID)

if "4" in args:
    inputList4 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/4/input", sanitiser=getInput.safeString).inputValues

    sortedInput = day4.puzzle1.sortInput(inputList4)

    shifts = [day4.puzzle1.Shift(events) for events in day4.puzzle1.parseInput(sortedInput)]
    guards = day4.puzzle1.reduceByGuard(shifts)

    sortedGuards = day4.puzzle1.sortGuardsByTotalSleepTime(guards)
    print(sortedGuards[0].ID * sortedGuards[0].getMaxMinute())

    maxGuard = day4.puzzle2.sortGuardsByAsleepMostAtSameMinute(guards)
    print(maxGuard[0].ID * maxGuard[0].getMaxMinute())

if "5" in args:
    inputList5 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/5/input", sanitiser=getInput.safeString).inputValues[0]
    
    reactedPolymer = day5.puzzle1.reactPolymer(inputList5)
    print(len(reactedPolymer))

    reactedPolymersRemovedUnit = day5.puzzle2.getAllReactedPolymersRemovingUnit(inputList5)
    sortedRemovedUnitPolymers = day5.puzzle2.sortPolymersByLen(reactedPolymersRemovedUnit)
    print(len(sortedRemovedUnitPolymers[0]))

if "6" in args:
    #inputList6 = getInput.InputValueReceiver(fileLocation="test6.txt", sanitiser=getInput.safeString).inputValues
    inputList6 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/6/input", sanitiser=getInput.safeString).inputValues

    grid = day6.puzzle1.parseInput(inputList6)
    numClosestToFiniteLocations = grid.getNumPointsClosestToFiniteLocations()
    largestFinite = grid.orderNumPointsClosestToLocation(numClosestToFiniteLocations)[0]

    print(largestFinite, numClosestToFiniteLocations[largestFinite])

    print(grid.getNumPointsCloserThanSumDistance(10000))

if "7" in args:
    #inputList7 = getInput.InputValueReceiver(fileLocation="test7.txt", sanitiser=getInput.safeString).inputValues
    #inputList7 = getInput.InputValueReceiver(fileLocation="day7.txt", sanitiser=getInput.safeString).inputValues
    inputList7 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/7/input", sanitiser=getInput.safeString).inputValues

    manual = day7.puzzle1.Manual(inputList7)
    manual.runAllSteps()

    print(manual.stepOrder)

    colabManual = day7.puzzle2.CollabarativeManual(inputList7, 5, baseTime=60)
    colabManual.runAllSteps()

    print(colabManual.time)

if "8" in args:
    #inputList8 = getInput.InputValueReceiver(fileLocation="test8.txt", sanitiser=getInput.safeString).inputValues[0]
    #inputList8 = getInput.InputValueReceiver(fileLocation="day8.txt", sanitiser=getInput.safeString).inputValues[0]
    inputList8 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/8/input", sanitiser=getInput.safeString).inputValues[0]
    parsedInput = day8.puzzle1.parseInput(inputList8)

    tree = day8.puzzle1.LicenceTree(parsedInput)
    tree.doTree()

    print(tree.sumMetadata())
    print(tree.getRootNode().getValue())

if "9" in args:
    #inputList9 = getInput.InputValueReceiver(fileLocation="test9.txt", sanitiser=getInput.safeString).inputValues[0]
    #inputList9 = getInput.InputValueReceiver(fileLocation="day9.txt", sanitiser=getInput.safeString).inputValues[0]
    inputList9 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/9/input", sanitiser=getInput.safeString).inputValues[0]

    parsedInput = day9.puzzle1.parseInput(inputList9)

    circle = day9.puzzle1.Circle(parsedInput[0], parsedInput[1])
    circle.playGame()
    print(circle.getHighestScorePlayer())

    bigCircle = day9.puzzle2.BigCircle(parsedInput[0], parsedInput[1])
    bigCircle.playGame()
    print(bigCircle.getHighestScorePlayer())

if "10" in args:
    #inputList10 = getInput.InputValueReceiver(fileLocation="test10.txt", sanitiser=getInput.safeString).inputValues
    #inputList10 = getInput.InputValueReceiver(fileLocation="day10.txt", sanitiser=getInput.safeString).inputValues
    inputList10 = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/10/input", sanitiser=getInput.safeString).inputValues

    sky = day10.puzzle1.Sky(inputList10)

    while not sky.checkCloseness():
        sky.moveStars()
    print("HIT at " + str(sky.time))
    print(sky)

if "11" in args:
    fuelCellSquare = day11.puzzle1.Square(2568)
    print fuelCellSquare.getMaxSquare(3)
    print fuelCellSquare.getMaxSquareOfSquares()
