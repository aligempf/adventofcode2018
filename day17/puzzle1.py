class Ground:
    def __init__(self, inputList):
        self.clayLocations = set()
        self.waterLocations = dict()
        self.springLocation = (500,0)
        for list in inputList:
            self.clayLocations = self.clayLocations.union(parseInputElement(list))
        self.yboundaries = (min(map(lambda location: location[1], self.clayLocations)), max(map(lambda location: location[1], self.clayLocations)))
        # self.yboundaries = (0, 294)
        self.waterStreams = set()
        # self.prevDirection = 1

    def getBoundary(self):
        minx = min(map(lambda location: location[0], self.getFilledLocations()))
        miny, maxy = self.yboundaries
        maxx = max(map(lambda location: location[0], self.getFilledLocations()))
        return ((minx, miny), (maxx, maxy))

    def __repr__(self):
        strRep = ""
        boundary = self.getBoundary()
        waterLocations = self.waterLocations
        for y in range(boundary[0][1], boundary[1][1]+1):
            strRep += "%i\t" %y
            for x in range(boundary[0][0], boundary[1][0]+1):
                if (x,y) == self.springLocation:
                    strRep += "+"
                elif (x,y) in self.clayLocations:
                    strRep += "#"
                elif (x,y) in waterLocations:
                    if waterLocations[(x,y)]:
                        strRep += "~"
                    else:
                        strRep += "|"
                else:
                    strRep += "."
            strRep += "\n"
        return strRep

    def addWater(self):
        stream = WaterStream(self.springLocation[0], self.springLocation[1], self)
        self.waterStreams.add(stream)
        unresolvedStreams = filter(lambda stream: not stream.resolved, self.waterStreams)

        while unresolvedStreams:
            stream = unresolvedStreams.pop()
            stream.resolveStream()
            unresolvedStreams = filter(lambda stream: not stream.resolved, self.waterStreams)

            for stream in self.waterStreams:
                if self.waterLocations:
                    self.waterLocations.update(stream.locations)
                else:
                    self.waterLocations = stream.locations
        self.waterLocations.pop(self.springLocation, None)
        realSettledWater = {water: True for water in filter(lambda location: not self.waterLocations[location], self.waterLocations)
                                if (self.waterLocations.get((water[0], water[1] + 1), None) or (water[0], water[1] + 1) in self.clayLocations)
                                    and (self.waterLocations.get((water[0], water[1] - 1), None) or (water[0], water[1] - 1) in self.clayLocations)}
        self.waterLocations.update(realSettledWater)
        realSettledWater = {water: True for water in filter(lambda location: not self.waterLocations[location], self.waterLocations)
                            if (self.waterLocations.get((water[0] + 1, water[1]), None) or (water[0] + 1, water[1]) in self.clayLocations)
                            and (self.waterLocations.get((water[0] - 1, water[1]), None) or (water[0] - 1, water[1]) in self.clayLocations)}
        self.waterLocations.update(realSettledWater)


    def getSetOfWater(self):
        return self.waterLocations

    def getSetOfWaterLocations(self):
        return self.waterLocations

    def getFilledLocations(self):
        return set(self.clayLocations.union(self.getSetOfWaterLocations()))

class WaterStream:
    def __init__(self, x, starty, ground, parent=None):
        self.x = x
        self.starty = starty
        self.endy = None
        self.locations = dict()
        self.ground = ground
        self.resolved = False
        self.parent = parent
        self.children = set()
        for y in range(starty, ground.yboundaries[1]+1):
            if (x, y) in ground.clayLocations:
                self.endy = y - 1
                break
            self.locations[(x,y)] = False
        if self.endy == None:
            self.endy = ground.yboundaries[1]+1
            self.resolved = True

    def resolveStream(self):
        spillover = [None, None]
        for child in self.children:
            child.resolveStream()
        if self.resolved:
            return
        for y in range(self.endy, 0, -1):
            index = 1
            checkDirection = [None, None]
            while True:
                if all(map(lambda direction: direction is not None, checkDirection)):
                    break
                if checkDirection[0] is None:
                    if (self.x - index, y) in self.ground.clayLocations:
                        checkDirection[0] = index - 1
                    elif (self.x - index, y + 1) not in self.ground.clayLocations and (self.x - index + 1, y + 1) in self.ground.clayLocations:
                        if (self.x - index - 1, y) not in self.ground.waterLocations and (self.x - index - 1, y) not in self.ground.clayLocations:
                            spillover[0] = (self.x - index, y)
                            checkDirection[0] = index
                if checkDirection[1] is None:
                    if (self.x + index, y) in self.ground.clayLocations:
                        checkDirection[1] = index - 1
                    elif (self.x + index, y + 1) not in self.ground.clayLocations and (self.x + index - 1, y + 1) in self.ground.clayLocations:
                        if (self.x + index + 1, y) not in self.ground.waterLocations and (self.x + index + 1, y) not in self.ground.clayLocations:
                            spillover[1] = (self.x + index, y)
                            checkDirection[1] = index
                index += 1
            if checkDirection[0] is not None and checkDirection[1] is not None:
                for x in range(self.x-checkDirection[0], self.x+checkDirection[1]+1):
                    self.locations[(x,y)] = True

            if any(map(lambda location: location is not None, spillover)):
                for x in range(self.x-checkDirection[0], self.x+checkDirection[1]+1):
                    self.locations[(x,y)] = False
                break
        self.resolved = True

        if not any(map(lambda location: location is not None, spillover)) and not self.endy == self.ground.yboundaries[1]+1:
            raise Exception

        for x in spillover:
            if x:
                if x not in self.ground.waterLocations:
                    newStream = WaterStream(x[0], x[1], self.ground, self)
                    self.ground.waterStreams.add(newStream)
                    self.children.add(newStream)
        self.ground.waterLocations.update(self.locations)

    def __repr__(self):
        return "Stream at " + str((self.x, self.starty))

def parseInputElement(element):
    firstLocationAxis = element.split("=")[0]
    firstLocation = [int(element.split("=")[1].split(', ')[0])]
    locationRange = map(int, element.split("=")[2].split(".."))
    x = firstLocation if firstLocationAxis == "x" else range(locationRange[0], locationRange[1]+1)
    y = firstLocation if firstLocationAxis == "y" else range(locationRange[0], locationRange[1]+1)
    return {(i, j) for i in x for j in y}