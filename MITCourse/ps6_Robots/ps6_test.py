from ps6 import *

if __name__ == "__main__":
    t = RectangularRoom(20,20)
    p = Position(2,3)
    p3 = Position(20,20)
    t.cleanTileAtPosition(p)
    print t.getNumCleanedTiles()
    p2 = t.getRandomPosition()
    print p2.x, p2.y
    print t.isPositionInRoom(p2)
    print t.isPositionInRoom(p3)
