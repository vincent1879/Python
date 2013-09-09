# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.matrix = {}
        self.width = width
        self.height = height
        l = [(x,y) for x in range(width) for y in range(height)]
        for i in l:
            self.matrix[i] = False

    def ResetRoom(self):
        for key in self.matrix.keys():
            self.matrix[key] = False
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = pos.getX()
        y = pos.getY()

        locX = int(math.floor(x))
        locY = int(math.floor(y))

        self.matrix[(locX, locY)] = True
        

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.matrix[(m,n)]
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self.matrix)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        cleanTileCount = 0
        for i in self.matrix.values():
            if i == True:
                cleanTileCount += 1
        return cleanTileCount

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.random() * self.width
        y = random.random() * self.height 
        return Position(x,y)
        

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()

        if x >= 0 and x < self.width and y >=0 and y < self.height:
            return True
        else:
            return False



class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = random.randrange(360)
        self.pos = room.getRandomPosition()
        self.room.cleanTileAtPosition(self.pos)


    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """

        return self.direction

        

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """

        self.pos = position
        

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """

        self.direction = direction
        

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        self.pos = self.pos.getNewPosition(self.direction, self.speed)
        self.room.cleanTileAtPosition(self.pos)



# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        while True:
            newPos = self.pos.getNewPosition(self.direction, self.speed)
            if self.room.isPositionInRoom(newPos):
                self.pos = newPos
                self.room.cleanTileAtPosition(self.pos)
                break
            else:
                self.direction = random.randrange(360)

        

# === Problem 3


def runSimulationVisual(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    totalStep = 0
    room = RectangularRoom(width, height)
    tilesNeedClean = int(room.getNumTiles() * min_coverage)


    for i in range(num_trials):

        room.ResetRoom()
        timeStep = 0
        tilesCleaned = 0
        robotList = []
        for i in range(num_robots):
            robotList.append(robot_type(room, speed))

        anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        
        while tilesCleaned < tilesNeedClean:

            for robot in robotList:
                robot.updatePositionAndClean()
            tilesCleaned = room.getNumCleanedTiles()
            # print tilesCleaned
            timeStep += 1

            anim.update(room, robotList)

        anim.done()
        totalStep += timeStep

    
    return float(totalStep) / num_trials

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    totalStep = 0
    room = RectangularRoom(width, height)
    tilesNeedClean = int(room.getNumTiles() * min_coverage)
    # print tilesNeedClean

    for i in range(num_trials):

        room.ResetRoom()
        timeStep = 0
        tilesCleaned = 0
        robotList = []
        for i in range(num_robots):
            robotList.append(robot_type(room, speed))

        while tilesCleaned < tilesNeedClean:

            for robot in robotList:
                robot.updatePositionAndClean()
            tilesCleaned = room.getNumCleanedTiles()
            # print tilesCleaned
            timeStep += 1

        totalStep += timeStep

    
    return float(totalStep) / num_trials

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20*20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20*20, 25*16, 40*10, 50*8, 80*5, and 100*4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    
    x = range(1,11)
    y = []

    for i in x:
        avg = runSimulation(i, 1.0, 20, 20, 0.8, 10, StandardRobot)
        y.append(avg)

    pylab.title('Simulation Robot Number against Cleaning Time')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('TimeStep')
    pylab.plot(x,y)
    pylab.show()



def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    t = [(20,20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    x = [float(w) / h for (w,h) in t]
    y = []
    for  ratio in t:
        avg = runSimulation(2, 1.0, ratio[0], ratio[1], 0.8, 100, StandardRobot)
        y.append(avg)

    pylab.title('Simulation Area w/h ratio against Cleaning Time')
    pylab.xlabel('Ratio of w/h')
    pylab.ylabel('TimeStep')
    pylab.plot(x,y,'ro')
    pylab.show()


# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        while True:
            self.direction = random.randrange(360)
            newPos = self.pos.getNewPosition(self.direction, self.speed)
            if self.room.isPositionInRoom(newPos):
                self.pos = newPos
                self.room.cleanTileAtPosition(self.pos)
                break


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    x = []
    y1 = []
    y2 = []
    areaList = [(a,a) for a in range(5,21)]
    for area in areaList:
        avg1 = runSimulation(2, 1.0, area[0], area[1], 1.0, 10, StandardRobot)
        avg2 = runSimulation(2, 1.0, area[0], area[1], 1.0, 10, RandomWalkRobot)
        y1.append(avg1)
        y2.append(avg2)

    x = [b[0] * b[1] for b in areaList]
    pylab.title('Compare Two robots with area growth')
    pylab.ylabel('TimeStep')
    pylab.xlabel('Area')
    pylab.plot(x,y1,'g')
    pylab.plot(x,y2,'r')
    pylab.show()

def showPlot4():

    x = range(1,21)
    y1 = []
    y2 = []
    for i in x:
        avg1 = runSimulation(i, 1.0, 20, 20, 1.0, 10, StandardRobot)
        avg2 = runSimulation(i, 1.0, 20, 20, 1.0, 10, RandomWalkRobot)
        y1.append(avg1)
        y2.append(avg2)

    pylab.title('Compare Two robots with robot number growth')
    pylab.ylabel('TimeStep')
    pylab.xlabel('Robots Number')
    pylab.plot(x,y1,'g')
    pylab.plot(x,y2,'r')
    pylab.show()



if __name__ == '__main__':
    showPlot4()