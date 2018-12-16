from collections import deque

class Map:
    def __init__(self, inputList):
        self.positions = {}
        self.goblins = set()
        self.elves = set()
        for y in range(len(inputList)):
            for x in range(len(inputList[y])):
                if inputList[y][x] == "#":
                    self.positions[(x,y)] = Position((x,y), self, True)
                else:
                    position = Position((x,y), self)
                    self.positions[(x,y)] = position
                    if inputList[y][x] == "E":
                        self.elves.add(Elf(position))
                    elif inputList[y][x] == "G":
                        self.goblins.add(Goblin(position))
        self.turns = 0
                

    def sortUnits(self):
        return readingOrder(self.elves.union(self.goblins))

    def __repr__(self):
        strRep = ""
        for y in range(self.getBoundary()[1]+1):
            for x in range(self.getBoundary()[0]+1):
                if self.positions[(x,y)].wall:
                    strRep += "#"
                elif self.positions[(x,y)] in self.getGoblinPositions():
                    strRep += "G"
                elif self.positions[(x,y)] in self.getElfPositions():
                    strRep += "E"
                else:
                    strRep += "."
            strRep += "\n"
        return strRep

    def getGoblinPositions(self):
        return set(goblin.position for goblin in self.goblins)

    def getElfPositions(self):
        return set(elf.position for elf in self.elves)

    def getUnfilledNeighbours(self, unit=None, position=None, filledPositions=None):
        if filledPositions is None:
            filledPositions = self.getFilledPositions()
        if unit is not None:
            return set(neighbour for neighbour in unit.getNeighbours() if neighbour not in filledPositions)
        else:
            return set(neighbour for neighbour in position.getNeighbours() if neighbour not in filledPositions)

    def getFilledPositions(self):
        return set(filter(lambda position: position.wall, self.positions.values())).union(self.getElfPositions()).union(self.getGoblinPositions())
        
    def getUnfilledPositions(self):
        return set(self.positions.values()).difference(self.getFilledPositions())

    def getBoundary(self):
        return (max(self.positions, key=lambda wall: wall[0])[0], max(self.positions, key=lambda wall: wall[1])[1])

    def turn(self):
        unfilledPositions = self.getUnfilledPositions()
        goblinPositions = self.getGoblinPositions()
        elfPositions = self.getElfPositions()

        units = self.sortUnits()

        for unit in units:
            if unit.HP <= 0:
                continue
            currentPosition = unit.position
            enemies = self.goblins if isinstance(unit, Elf) else self.elves
            enemyPositions = goblinPositions if isinstance(unit, Elf) else elfPositions
            allyPositions = goblinPositions if isinstance(unit, Goblin) else elfPositions

            if not enemies:
                break

            allyPositions.remove(currentPosition)
            unfilledPositions.add(currentPosition)

            nextPosition = unit.getNextStep(enemies, unfilledPositions)
            unfilledPositions.remove(nextPosition)
            allyPositions.add(nextPosition)
            unit.moveToPosition(nextPosition)
                
            combatTarget = unit.decideTarget(enemies)
            if combatTarget:
                unit.hitTarget(combatTarget)
                if combatTarget.HP <= 0:
                    self.removeUnit(combatTarget)
                    enemyPositions.remove(combatTarget.position)
                    unfilledPositions.add(combatTarget.position)

        if self.elves and self.goblins:
            self.turns += 1

    def removeUnit(self, unit):
        if isinstance(unit, Elf):
            self.elves.remove(unit)
        else:
            self.goblins.remove(unit)

class Position:
    def __init__(self, position, board, isWall=False):
        self.position = position
        self.wall = isWall
        self.board = board
        self.neighbours = None

    def __getitem__(self, item):
        return self.position[item]

    def __hash__(self):
        return hash((self.position[0], self.position[1], self.wall))

    def __repr__(self):
        return str(self.position) + " " + str(self.wall)

    def __getNeighbours__(self):
        return set([self.board.positions[(self[0]+1,self[1])],self.board.positions[(self[0]-1,self[1])],
                        self.board.positions[(self[0],self[1]+1)],self.board.positions[(self[0],self[1]-1)]])

    def getNeighbours(self):
        if self.neighbours == None:
            self.neighbours = self.__getNeighbours__()
        return self.neighbours
    
    def getUnfilledNeighbours(self, unfilledPositions=None):
        if unfilledPositions == None:
            unfilledPositions = self.board.getUnfilledPositions()
        return self.getNeighbours() & unfilledPositions

class Unit:
    def __init__(self, position, HP, AP):
        self.HP = HP
        self.position = position
        self.AP = AP

    def getNeighbours(self):
        return self.position.getNeighbours()

    def getUnfilledNeighbours(self, unfilledPositions=None):
        return self.position.getUnfilledNeighbours(unfilledPositions)

    def __getitem__(self, item):
        return self.position[item]

    def stepsToPosition(self, position):
        return sum(abs(self.position[i] - position[i]) for i in range(len(self.position)))

    def moveToPosition(self, position):
        self.position = position

    def decideTarget(self, enemies):
        possibleTargets = filter(lambda enemy: enemy.position in self.getNeighbours(), enemies)
        if possibleTargets:
            lowestHP = min(possibleTargets, key=lambda target: target.HP).HP
            lowestHPTargets = filter(lambda enemy: enemy.HP == lowestHP, possibleTargets)
            return readingOrder(lowestHPTargets)[0]
        else:
            return None

    def hitTarget(self, enemy):
        enemy.HP -= self.AP

    def getNextStep(self, enemies, unfilledPositions):
        if filter(lambda enemy: enemy.position in self.getNeighbours(), enemies):
            return self.position
        targets = self.acquireTarget(enemies, unfilledPositions)
        if targets:
            orderedTarget = sorted(targets, key=lambda target: target.target)[0].target
            return readingOrder(map(self.getFirstNodeOfPath, filter(lambda target: target.target == orderedTarget,targets)))[0].position
        else:
            return self.position

    def acquireTarget(self, enemies, unfilledPositions):
        currentSearchPathDistances = {}
        for enemy in enemies:
            for enemyNeighbour in enemy.getUnfilledNeighbours(unfilledPositions):
                if currentSearchPathDistances:
                    searchPath = self.getToPosition(enemyNeighbour, unfilledPositions, min(currentSearchPathDistances))
                    if searchPath.valid:
                        if searchPath:
                            if searchPath.pathDistance not in currentSearchPathDistances:
                                currentSearchPathDistances[searchPath.pathDistance] = [searchPath]
                            elif searchPath:
                                currentSearchPathDistances[searchPath.pathDistance].append(searchPath)
                else:
                    searchPath = self.getToPosition(enemyNeighbour, unfilledPositions)
                    if searchPath.valid:
                        currentSearchPathDistances[searchPath.pathDistance] = [searchPath]
        if currentSearchPathDistances:
            return currentSearchPathDistances[min(currentSearchPathDistances)]
        else:
            return None

    def getToPosition(self, position, unfilledPositions, maxLength=None):
        currentNode = SearchNode(self.position)
        nodes = {self.position.position: currentNode}

        while not currentNode.position.position == position.position:
            for neighbour in currentNode.getUnfilledNeighbours(unfilledPositions):
                if neighbour.position not in nodes:
                    nodes[neighbour.position] = SearchNode(neighbour, currentNode)
                else:
                    nodes[neighbour.position].addPreviousNode(currentNode)
            listToVisit = filter(lambda node: not node.visited, sorted(nodes.values(), key=lambda node: node.distance))
            if not listToVisit:
                return SearchPath(nodes, position, False)
            currentNode = listToVisit[0]
            if maxLength and currentNode.distance > maxLength:
                return SearchPath(nodes, position, False)

        listToVisit = filter(lambda node: not node.visited,
            filter(lambda node: node.distance < nodes[position.position].distance,
            nodes.values()))

        for node in listToVisit:
            for neighbour in node.getUnfilledNeighbours(unfilledPositions):
                if neighbour.position == position.position:
                    nodes[position.position].addPreviousNode(node)
        return SearchPath(nodes, position, True)

    def getFirstNodeOfPath(self, searchPath):
        if searchPath.valid:
            return readingOrder(searchPath[1])[0]
        else:
            return None

class SearchPath:
    def __init__(self, nodes, target, valid):
        if not valid:
            self.valid = False
            return
        distances = {nodes[target.position].distance: [nodes[target.position]]}
        for distance in range(nodes[target.position].distance - 1, 0, -1):
            distances[distance] = []
            for node in distances[distance + 1]:
                neighbours = nodes[node.position.position].getNeighbours()
                for neighbour in neighbours:
                    if neighbour.position in nodes:
                        if nodes[neighbour.position].distance == distance:
                            distances[distance].append(nodes[neighbour.position])
        self.target = target
        self.distances = distances
        self.pathDistance = max(self.distances)
        self.valid = valid

    def __repr__(self):
        return str(self.distances)

    def __getitem__(self, item):
        return self.distances[item]

class SearchNode:
    def __init__(self, position, previousNode=None):
        self.position = position
        self.visited = False
        if previousNode:
            self.previousNodes = set([previousNode])
            self.distance = previousNode.distance + 1
        else:
            self.previousNodes = None
            self.distance = 0

    def addPreviousNode(self, node):
        if node.distance < self.distance:
            self.previousNodes.add(node)

    def getNeighbours(self):
        return self.position.getNeighbours()

    def getUnfilledNeighbours(self, unfilledPositions):
        self.visited = True
        return self.position.getUnfilledNeighbours(unfilledPositions)

    def __repr__(self):
        return str(self.visited) + " " + str(self.position) + " " + str(self.distance)

    def __getitem__(self, item):
        return self.position[item]

class Elf(Unit):
    def __init__(self, position):
        Unit.__init__(self, position, 200, 3)
        self.enemies = set([Goblin])

class Goblin(Unit):
    def __init__(self, position):
        Unit.__init__(self, position, 200, 3)
        self.enemies = set([Elf])

def readingOrder(positions):
    return sorted(positions, key=lambda position: (position[1], position[0]))
    