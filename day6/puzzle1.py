def parseInput(inputList):
    a = [tuple(map(int, i.split(", "))) for i in inputList]
    return Grid(a)

class Grid:
    def __init__(self, locations):
        self.locations = {i: Location(locations[i]) for i in range(len(locations))}
        (self.minCoords, self.maxCoords) = self.getBorderCoords()
        self.pointClosestLocations = self.getClosestLocations()

    def __repr__(self):
        gridRep = ""
        for y in range(self.minCoords[1], self.maxCoords[1] + 1):
            for x in range(self.minCoords[0], self.maxCoords[0] + 1):
                closest = Point((x,y)).sortLocationsByDistance(Point((x,y)).distanceFromLocations(self))[0]
                if closest or closest == 0:
                    gridRep += str(closest)
                else:
                    gridRep += "."
            gridRep += "\n"
        return gridRep

    def getBorderCoords(self):
        minCoord = [0,0]
        maxCoord = [0, 0]
        for point in self.locations.values():
            minCoord[0] = min(minCoord[0], point[0])
            minCoord[1] = min(minCoord[1], point[1])
            maxCoord[0] = max(maxCoord[0], point[0])
            maxCoord[1] = max(maxCoord[1], point[1])
        return (tuple(minCoord), tuple(maxCoord))

    def getClosestLocations(self):
        return {
            Point((x,y)): Point((x,y)).sortLocationsByDistance(
                    Point((x,y)).distanceFromLocations(self)
                )[0] 
            for x in range(self.minCoords[0], self.maxCoords[0]+1)
            for y in range(self.minCoords[1], self.maxCoords[1]+1)
        }

    def getSumOfDistanceFromLocations(self):
        # for puzzle 2
        return {
            Point((x,y)): sum(Point((x,y)).distanceFromLocations(self).values())
                for x in range(self.minCoords[0], self.maxCoords[0]+1)
                for y in range(self.minCoords[1], self.maxCoords[1]+1)
        }

    def getNumPointsCloserThanSumDistance(self, max):
        # for puzzle 2
        sumDistances = self.getSumOfDistanceFromLocations()
        return len(filter(lambda x: sumDistances[x] < max, sumDistances))

    def getNumPointsClosestToLocation(self):
        return {loc: len(self.filterPointsByLocation(loc)) for loc in self.locations}

    def isLocationInfinite(self, loc):
        rightEdge = (len(self.filterLocationPointsByColumn(loc, self.maxCoords[1] - 1)), len(self.filterLocationPointsByColumn(loc, self.maxCoords[1])))
        leftEdge = (len(self.filterLocationPointsByColumn(loc, self.minCoords[1] + 1)), len(self.filterLocationPointsByColumn(loc, self.minCoords[1])))
        topEdge = (len(self.filterLocationPointsByRow(loc, self.maxCoords[0] - 1)), len(self.filterLocationPointsByRow(loc, self.maxCoords[0])))
        bottomEdge = (len(self.filterLocationPointsByRow(loc, self.minCoords[0] - 1)), len(self.filterLocationPointsByRow(loc, self.minCoords[0])))
        expandingRight = rightEdge[0] <= rightEdge[1] and not rightEdge[1] == 0
        expandingLeft = leftEdge[0] <= leftEdge[1] and not leftEdge[1] == 0 
        expandingDown = bottomEdge[0] <= bottomEdge[1] and not bottomEdge[1] == 0 
        expandingUp =   topEdge[0] <= topEdge[1] and not topEdge[1] == 0
        return expandingDown or expandingLeft or expandingRight or expandingUp

    def filterPointsByLocation(self, loc):
        return filter(lambda a: self.pointClosestLocations[a] == loc, self.pointClosestLocations.keys())

    def filterLocationPointsByColumn(self, loc, column):
        return filter(lambda x: x.isInColumn(column), self.filterPointsByLocation(loc))

    def filterLocationPointsByRow(self, loc, row):
        return filter(lambda x: x.isInRow(row), self.filterPointsByLocation(loc))

    def infiniteLocations(self):
        return set(filter(self.isLocationInfinite, self.locations))

    def finiteLocations(self):
        return set(self.locations.keys()).difference(self.infiniteLocations())

    def getNumPointsClosestToFiniteLocations(self):
        return {loc: len(self.filterPointsByLocation(loc)) for loc in self.finiteLocations()}

    def orderNumPointsClosestToLocation(self, numPointsClosest, reverse=True):
        return sorted(numPointsClosest, key=lambda a: numPointsClosest[a], reverse=reverse)

class Point:
    def __init__(self, coords, location=None):
        self.coords = tuple(map(int, coords))
        self.location = location

    def __repr__(self):
        location = "with location " if self.location else ""
        return "Point " + location + "at " + str(self.coords)

    def __getitem__(self, item):
        return self.coords[item]

    def __hash__(self):
        return hash(self.coords)

    def distanceFromLocations(self, grid):
        return {location: grid.locations[location].distance(self) for location in grid.locations}

    def sortLocationsByDistance(self, locDistances):
        if locDistances.values().count(min(locDistances.values())) > 1:
            return [None]
        return sorted(locDistances, key=lambda a: locDistances[a])

    def distance(self, point):
        return sum(abs(self[i] - point[i]) for i in range(2))

    def isInColumn(self, column):
        return self[1] == column

    def isInRow(self, row):
        return self[0] == row

class Location(Point):
    def __init__(self, point):
        self.coords = tuple(map(int, point))
        self.point = tuple(map(int, point))

    def __repr__(self):
        return "Location at " + str(self.point)
