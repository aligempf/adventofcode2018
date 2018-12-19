def parseInput(inputList):
    return {TestCase(inputList[i:i+3]) for i in range(len(inputList)) if "Before: " in inputList[i]}

class TestCase:
    def __init__(self, case):
        self.before = map(int, case[0].split("[")[1][:-1].split(", "))
        self.code = map(int, case[1].split(" "))
        self.after = map(int, case[2].split("[")[1][:-1].split(", "))
        self.beforecpu = CPU(self.before)
        self.aftercpu = CPU(self.after)

    def __repr__(self):
        return "Before: " + str(self.before) + "\n" + str(self.code) + "\nAfter: " + str(self.after)

    def __call__(self, function):
        beforecpu = CPU(self.before)
        function(self.code, beforecpu)
        return beforecpu == self.aftercpu

class CPU:
    def __init__(self, registerValues=None):
        if registerValues:
            self.registerValues = [value for value in registerValues]
        else:
            self.registerValues = [0, 0, 0, 0]

    def __getitem__(self, item):
        return self.registerValues[item]

    def __eq__(self, other):
        return self.registerValues == other.registerValues

    def __setitem__(self, key, value):
        self.registerValues[key] = value

    def __repr__(self):
        return str(self.registerValues)

def addr(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]] + cpu[opcode[2]]

def addi(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]] + opcode[2]

def mulr(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]] * cpu[opcode[2]]

def muli(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]] * opcode[2]

def banr(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]] & cpu[opcode[2]]

def bani(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]] & opcode[2]

def borr(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]] | cpu[opcode[2]]

def bori(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]] | opcode[2]

def setr(opcode, cpu):
    cpu[opcode[3]] = cpu[opcode[1]]

def seti(opcode, cpu):
    cpu[opcode[3]] = opcode[1]

def gtir(opcode, cpu):
    cpu[opcode[3]] = 1 if opcode[1] > cpu[opcode[2]] else 0

def gtri(opcode, cpu):
    cpu[opcode[3]] = 1 if cpu[opcode[1]] > opcode[2] else 0

def gtrr(opcode, cpu):
    cpu[opcode[3]] = 1 if cpu[opcode[1]] > cpu[opcode[2]] else 0

def eqir(opcode, cpu):
    cpu[opcode[3]] = 1 if opcode[1] == cpu[opcode[2]] else 0

def eqri(opcode, cpu):
    cpu[opcode[3]] = 1 if cpu[opcode[1]] == opcode[2] else 0

def eqrr(opcode, cpu):
    cpu[opcode[3]] = 1 if cpu[opcode[1]] == cpu[opcode[2]] else 0

FUNCTIONS = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
