LEFT, STRAIGHT, RIGHT = 0, 1, 2

class Cart:
    def __init__(self, location, direction):
        self.location = location
        self.direction = Direction(direction)
        self.nextIntersection = 0

    def takeIntersection(self):
        self.direction = self.direction + self.nextIntersection
        self.nextIntersection = (self.nextIntersection + 1) % 3

    def __repr__(self):
        return "Cart at " + str(self.location) + " travelling in direction " + str(self.direction) + " " + self.getString()

    def getString(self):
        return self.direction.getString()

    def nextLocation(self):
        return tuple([self.location[i] + self.direction[i] for i in range(len(self.location))])

    def moveOnTrack(self, track):
        self.location = self.nextLocation()
        if track.trackDirection == 2:
            self.takeIntersection()
        else:
            self.direction = track + self.direction

class Direction:

    CARTREPRESENTATION = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}
    DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    def __init__(self, direction):
        self.direction = direction

    def __getitem__(self, item):
        return self.direction[item]

    def __add__(self, other):
        if other == STRAIGHT:
            return self
        if other == LEFT:
            return Direction(Direction.DIRECTIONS[(Direction.DIRECTIONS.index(self.direction) + 1) % len(Direction.DIRECTIONS)])
        if other == RIGHT:
            return Direction(Direction.DIRECTIONS[(Direction.DIRECTIONS.index(self.direction) - 1)])

    def __repr__(self):
        return str(self.direction)

    def getString(self):
        return self.CARTREPRESENTATION.keys()[self.CARTREPRESENTATION.values().index(self.direction)]

    def isVertical(self):
        return self.direction == self.DIRECTIONS[1] or self.direction == self.DIRECTIONS[3]

    def isHorizontal(self):
        return self.direction == self.DIRECTIONS[0] or self.direction == self.DIRECTIONS[2]

class TrackPiece:

    TRACKDIRECTIONS = {"|": 0, "-": 1, "+": 2, "\\": 3, "/": 4}

    def __init__(self, piece, location):
        self.trackDirection = self.TRACKDIRECTIONS[piece]
        self.location = location
        self.intersection = True if piece == "+" else False
        self.curve = True if self.trackDirection > 2 else False

    def __add__(self, other):
        if self.trackDirection == 0 or self.trackDirection == 1:
            return other + STRAIGHT
        if self.trackDirection == 3 and other.isVertical():
            return other + LEFT
        if self.trackDirection == 3 and other.isHorizontal():
            return other + RIGHT
        if self.trackDirection == 4 and other.isHorizontal():
            return other + LEFT
        if self.trackDirection == 4 and other.isVertical():
            return other + RIGHT

    def __repr__(self):
        return self.getString()

    def getString(self):
        return self.TRACKDIRECTIONS.keys()[self.TRACKDIRECTIONS.values().index(self.trackDirection)]

class Track:
    def __init__(self, inputList):
        (self.carts, self.track) = self.getTrack(inputList)
        self.boundary = (max(self.track, key=lambda piece: piece.location[0]).location[0], max(self.track, key=lambda piece: piece.location[1]).location[1])
        self.collision = False
        self.time = 0

    def getTrack(self, inputList):
        carts = set()
        track = set()
        for y in range(0, len(inputList)):
            for x in range(0, len(inputList[y])):
                if inputList[y][x] not in Direction.CARTREPRESENTATION.keys() and inputList[y][x] not in TrackPiece.TRACKDIRECTIONS:
                    continue
                elif inputList[y][x] in TrackPiece.TRACKDIRECTIONS:
                    track.add(TrackPiece(inputList[y][x], (x, y)))
                elif inputList[y][x] in Direction.CARTREPRESENTATION.keys():
                    cart = Cart((x,y), Direction.CARTREPRESENTATION[inputList[y][x]])
                    carts.add(cart)
                    if cart.direction.isVertical():
                        track.add(TrackPiece("|", (x, y)))
                    else:
                        track.add(TrackPiece("-", (x, y)))
        return carts, track

    def getTrackAtLocation(self, location):
        return filter(lambda piece: piece.location == location, self.track)[0]

    def tick(self, cartRemoval=False):
        cartsForRemoval = set()
        sortedCarts = sorted(self.carts, key=lambda cart: (cart.location[1], cart.location[0]))
        for cart in sortedCarts:
            cart.moveOnTrack(self.getTrackAtLocation(cart.nextLocation()))
            cartLocations = {otherCart.location: otherCart for otherCart in sortedCarts if not otherCart == cart}
            if cart.location in cartLocations:
                print("CRASH AT " + str(cart.location))
                self.collision = True
                if cartRemoval:
                    cartsForRemoval.add(cart)
                    cartsForRemoval.add(cartLocations[cart.location])
                    print("CARTS REMOVED FROM " + str(cart) + ", " + str(cartLocations[cart.location]))
            else:
                cartLocations[cart.location] = cart
        self.time += 1
        self.carts = set(sortedCarts).difference(cartsForRemoval)

    def __repr__(self):
        stringRep = ""
        carts = {cart.location: cart for cart in self.carts}
        track = {piece.location: piece for piece in self.track}
        for y in range(self.boundary[1] + 1):
            for x in range(self.boundary[0] + 1):
                if (x, y) in carts:
                    stringRep += carts[(x, y)].getString()
                elif (x, y) in track:
                    stringRep += track[(x, y)].getString()
                else:
                    stringRep += " "
            stringRep += "\n"
        return stringRep
