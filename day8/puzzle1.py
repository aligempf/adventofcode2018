def parseInput(inputString):
    return map(int, inputString.split(" "))

class LicenceLetter:
    def __init__(self, ID, numChildren, numMetadata):
        self.ID = ID
        self.numChildren = numChildren
        self.numMetadata = numMetadata
        self.children = []
        self.parent = None
        self.metadata = []
        self.value = None
        self.resolved = False
        if len(self.children) == self.numChildren:
            self.resolved = True

    def __hash__(self):
        return hash(self.ID)

    def addChild(self, child):
        self.children.append(child)
        if len(self.children) == self.numChildren:
            self.resolved = True

    def addParent(self, parent):
        parent.addChild(self)
        self.parent = parent

    def addMetadata(self, metadata):
        self.metadata = metadata

    def sumMetadata(self):
        return sum(self.metadata)

    def getValue(self):
        # for puzzle 2
        if not self.value == None:
            return self.value
        if len(self.children) == 0:
            self.value = self.sumMetadata()
            return self.value
        self.value = 0
        for metadatum in self.metadata:
            if metadatum - 1 < len(self.children):
                self.value += self.children[metadatum - 1].getValue()
        return self.value

class LicenceTree:
    def __init__(self, parsedInput):
        self.treeList = parsedInput
        self.currentIndex = 0
        self.currentID = 0
        self.tree = set()

    def doTree(self, parent=None):
        currentTree = set()
        thisLetter = LicenceLetter(self.currentID, self.treeList[self.currentIndex], self.treeList[self.currentIndex + 1])
        self.currentID += 1
        if parent:
            thisLetter.addParent(parent)
        currentTree.add(thisLetter)
        self.currentIndex += 2
        if thisLetter.numChildren > 0:
            for child in range(thisLetter.numChildren):
                self.doTree(thisLetter)
        thisLetter.addMetadata(self.treeList[self.currentIndex:self.currentIndex+thisLetter.numMetadata])
        self.currentIndex += thisLetter.numMetadata
        self.tree = self.tree.union(currentTree)
        return thisLetter

    def sumMetadata(self):
        return sum(map(lambda letter: letter.sumMetadata(), self.tree))

    def getRootNode(self):
        return filter(lambda node: node.parent == None, self.tree)[0]
