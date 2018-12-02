import day1.puzzle1
import day1.puzzle2
import day2.puzzle1
import day2.puzzle2
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
    inputList2 = inputList = getInput.InputValueReceiver(url="https://adventofcode.com/2018/day/2/input", sanitiser=getInput.safeString).inputValues

    boxCheckSum = day2.puzzle1.boxCheckSum(inputList2)
    print(boxCheckSum)

    commonBoxLetters = day2.puzzle2.commonBoxLetters(inputList2)
    print(commonBoxLetters)
