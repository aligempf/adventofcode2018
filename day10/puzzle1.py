class Star:
    def __init__(self, inputInit, id):
        self.id = id
        self.position = tuple(map(int,inputInit.split("<")[1].split(">")[0].strip(" ").split(", ")))
        self.velocity = tuple(map(int,inputInit.split("<")[2].split(">")[0].strip(" ").split(", ")))

    def __eq__(self, other):
        return self.position == other

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return str(self.id) + ": " + str(self.position)

    def move(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])


class Sky:
    def __init__(self, inputList):
        self.stars = set(Star(inputList[id], id) for id in range(len(inputList)))
        self.maxLocation = (0, 0)
        self.minLocation = (0, 0)
        self.time = 0

    def getBoundaryLocation(self):
        minLocation = [None, None]
        maxLocation = [None, None]
        for star in self.stars:
            if minLocation[0] == None:
                minLocation = list(star.position)
                maxLocation = list(star.position)
            maxLocation[0] = max(maxLocation[0], star.position[0])
            maxLocation[1] = max(maxLocation[1], star.position[1])
            minLocation[0] = min(minLocation[0], star.position[0])
            minLocation[1] = min(minLocation[1], star.position[1])
        self.maxLocation = tuple(maxLocation)
        self.minLocation = tuple(minLocation)

    def stringRep(self):
        selfString = ""
        self.getBoundaryLocation()
        locations = self.getStarLocations()
        for y in range(self.minLocation[1], self.maxLocation[1] + 1):
            for x in range(self.minLocation[0], self.maxLocation[0] + 1):
                if (x, y) in locations:
                    selfString += "*"
                else:
                    selfString += " "
            selfString += "\n"
        return selfString

    def __repr__(self):
        return self.stringRep()

    def getStarLocations(self):
        return {star.position: star for star in self.stars}

    def moveStars(self):
        map(lambda star: star.move(), self.stars)
        self.time += 1
        #return self.stringRep()

    def checkCloseness(self, fraction=0.8):
        starLocations = self.getStarLocations()
        a = [True for star in self.stars for i in range(-1,1) for j in range(-1,1) if not i == j == 0 if (star.position[0] + i, star.position[1] + j) in starLocations]
        return len(a) > len(starLocations) * fraction
