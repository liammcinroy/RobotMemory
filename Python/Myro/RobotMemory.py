#-------------------------------------------------------------------------------
# Name:        Robot Memory
# Purpose:     Stores memory about where robot has been
# Author:      Liam McInory
# Created:     06/03/2014
# Copyright:   (c) Liam 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
from __future__ import division
from math import *
import Myro

def enum(**enums):
    return type('Enum', (), enums)

MemoryType = enum(Unknown=0, Visited=1, OffGrid=-1) #add more if you want



class RobotMemory:

    Plot = [[]]
    Speed = 0.5

    X = 0
    Y = 0

    __MidpointX = 0
    __MidpointY = 0

    __X = 0
    __Y = 0

    __TowardsX = 0
    __TowardsY = 0

    __Scale = 0.5


    #initialize robot, and create memory
    def __init__ (self, comPort = 3, width = 250, height = 250, speed = 0.5, scale = 0.5, lookX = 0, lookY = 1):
        #set global variables
        self.Speed = speed
        self.__Scale = scale

        self.__TowardsX = lookX
        self.__TowardsY = lookY

        self.__MidpointX = width / 2
        self.__MidpointY = height / 2

        multiplyBy = int(1.0 / scale)

        multiplyBy = int(1.0 / scale)

        self.Plot = [[MemoryType.Unknown] * width * multiplyBy for col in range(height * multiplyBy)]

        self.__MidpointX *= multiplyBy
        self.__MidpointY *= multiplyBy

        Myro.init("COM" + str(comPort))


    #set midpoint, and current coordinates
    def start(self, x, y):
        self.__X = x + self.__MidpointX
        self.__Y = y + self.__MidpointY

        self.X = x
        self.Y = y

        self.__TowardsX += self.__MidpointX
        self.__TowardsY += self.__MidpointY

        self.Plot[(int) (floor(self.__X))][(int) (floor(self.__Y))] = MemoryType.Visited


    #Turn a specified degrees
    def turn(self, theta):
        #3 = 1.5s/0.5speed = 90 degrees
        time90 = 3 * abs(self.Speed)
        time = time90 / abs(theta)

        left = 0

        if (theta > 0):
            left = 0

        if (left == 0):
            Myro.robot.turnLeft(time, abs(self.Speed))
        else:
            Myro.robot.turnRight(time, abs(self.Speed))

        #get true angle
        if (self.getSlope == 0):
            if (self.__TowardsX < self.__X):
                theta = 180 - theta
        else:
            theta = degrees(atan(self.getSlope())) - theta

        #get rotation values
        theta *= (pi / 180)
        sina = sin(theta)
        cosa = cos(theta)

        #origin points
        pX = self.__TowardsX - self.__X
        pY = self.__TowardsY - self.__Y

        self.__TowardsX = (cosa * pX - sina * pY) + self.__X
        self.__TowardsY = (sina * pX + cosa * pY) + self.__Y


    #move forward
    def goForward(self, duration):
        #if line is up and down
        if (self.__TowardsX - self.__X == 0):
            Myro.robot.motors(self.Speed, self.Speed)
            Myro.wait(abs(duration))
            Myro.robot.stop()
            #get the amount of points forward
            divisible = duration // self.__Scale

            if (self.__TowardsY > self.__Y):
                #add them to the direction
                self.__TowardsY += divisible
                tempY = self.__Y

                #add them to plot
                for y in xrange(self.__Y + self.__Scale, divisible + tempY + self.__Scale):
                    if (y % self.__Scale == 0):
                        try:
                            self.Plot[(int) (self.__X)][y] = MemoryType.Visited
                        except IndexError:
                            print("Error: Ran out of space. Expanding the plot\r\n")
                            self.ExpandPlot(5)
                            y -= 1

                #increase y
                self.__Y += divisible
                self.Y += divisible
                return

            else:
                #subtract them from the direction
                self.__TowardsY -= divisible
                tempY = self.__Y

                #add them to plot
                for y in xrange(self.__Y - divisible,  tempY + self.__Scale):
                    if (y % self.__Scale == 0):
                        try:
                            self.Plot[(int) (self.__X)][y] = MemoryType.Visited
                        except IndexError:
                            print("Error: Ran out of space. Expanding the plot\r\n")
                            self.ExpandPlot(5)
                            y -= 1

                #increase y
                self.__Y -= divisible
                self.Y -= divisible
                return


        #calc slope
        slope = (self.__TowardsY - self.__Y) / (self.__TowardsX - self.__X)
        tempX = self.__X
        tempY = self.__Y

        #go forward
        Myro.robot.motors(self.Speed, self.Speed)
        Myro.wait(abs(duration))

        Myro.robot.stop()

        #get the amount of points forward
        divisible = duration // self.__Scale

        #add them to the direction
        self.__TowardsX += divisible
        self.__TowardsY += divisible
        divisible = duration / self.__Scale

        Xs = []
        Ys = []

        if (slope >= 0):
            #positive slope
            for x in xrange(self.__X + self.__Scale, (tempX + divisible) + self.__Scale, self.__Scale):
                #get point
                y = (slope * (x - self.__X)) + self.__Y
                #find out if it is a plottable point
                if (y % self.__Scale == 0.0):
                    Xs.append(int(x))
                    Ys.append(int(y))

        else:
            #negative slope
            for x in xrange((tempX - divisible), self.__X, self.__Scale):
                #get point
                y = (slope * (x - self.__X)) + self.__Y
                #find out if it is a plottable point
                if (y % self.__Scale == 0.0):
                    Xs.append(int(x))
                    Ys.append(int(y))

        #Plot the points
        for i in xrange(0, len(Xs)):
            try:
                self.Plot[Xs[i]][Ys[i]] = MemoryType.Visited
            except IndexError:
                print("Error: Ran out of space. Expanding the plot.\r\n")
                self.ExpandPlot(5)
                i -= 1

        multiplyBy = 1.0 / self.__Scale

        if (slope >= 0):
            try:
                self.__X = Xs[len(Xs) - 1]
                self.__Y = Ys[len(Ys) - 1]
            except IndexError:
                print("Error: No measurable progression.\r\n")

        else:
            try:
                self.__X = Xs[0]
                self.__Y = Ys[0]
            except IndexError:
                print("Error: No measurable progression.\r\n")

        self.X = self.__X - self.__MidpointX
        self.Y = self.__Y - self.__MidpointY

    def curve(self, speedLeft, speedRight, duration): #TODO correct screwed up direction after curve
        #set temp
        tempX = self.__X
        tempY = self.__Y

        #set scale
        greaterSpeed = 0
        lesserSpeed = 0
        if (abs(speedLeft) > abs(speedRight)):
            greaterSpeed = speedLeft
            lesserSpeed = speedRight
        elif (abs(speedRight) > abs(speedLeft)):
            greaterSpeed = speedRight
            lesserSpeed = speedLeft
        else:
            duration = (duration / self.Speed) * speedLeft
            self.goForward(duration)
            return

        #move robot
        Myro.robot.motors(speedLeft, speedRight)
        Myro.wait(abs(duration))
        Myro.robot.stop()

        stretch = (1 / self.__Scale) * (greaterSpeed / lesserSpeed)

        divisible = duration // self.__Scale

        Xs = []
        Ys = []
        tempXs = []
        tempYs = []

        overAfterPoint = False

        timesOver = 1
        maxAmount = tempX + divisible + self.__Scale
        minAmount = self.__X + self.__Scale
        #stretch
        for x in xrange(minAmount, maxAmount, self.__Scale):
            #get point
            try:
                y = stretch * sqrt(1 - pow(((x - self.__X - stretch) / stretch), 2)) + self.__Y
                overAfterPoint = True
            except ValueError: #Support for > half circle turns
                if overAfterPoint == True:
                    try:
                        x -= (timesOver * self.__Scale + timesOver)
                        y = -stretch * (sqrt(1 - pow(((x - self.__X - stretch) / stretch), 2))) + self.__Y
                        timesOver += 1
                        maxAmount -= x
                    except ValueError:
                        continue
                else:
                    continue
            #find out if it is a plottable point
            tempXs.append(x)
            tempYs.append(y)

        theta = 90 - degrees(atan(self.getSlope()))

        sina = sin(theta)
        cosa = cos(theta)
    
        for i in xrange(0, len(tempXs)):
            pX = self.__X - self.__MidpointX
            pY = self.__Y - self.__MidpointY

            tempXs[i] = (cosa * pX - sina * pY) + tempXs[i]
            tempYs[i] = (sina * pX + cosa * pY) + tempYs[i]

            if (tempXs[i] % self.__Scale == 0 and tempYs[i] % self.__Scale == 0):
                Xs.append(tempXs[i])
                Ys.append(tempYs[i])

        #Plot the points
        for i in xrange(0, len(Xs)):
            try:
                self.Plot[int(Xs[i])][int(Ys[i])] = MemoryType.Visited
            except IndexError:
                print("Error: Ran out of space. Expanding the plot.\r\n")
                self.ExpandPlot(5)
                i -= 1

        multiplyBy = 1.0 / self.__Scale

        if (stretch >= 0):
            try:
                self.__X = Xs[len(Xs) - 1]
                self.__Y = Ys[len(Ys) - 1]
            except IndexError:
                print("Error: No measurable progression.\r\n")
                return

        else:
            try:
                self.__X = Xs[0]
                self.__Y = Ys[0]
            except IndexError:
                print("Error: No measurable progression.\r\n")
                return

        #add it to the direction using derivative
        slope = 0
        try:
            slope = (tempX - self.__X)/ (stretch * sqrt(1 - (pow(tempX - self.__X, 2)/pow(stretch, 2))))
        except ValueError:
            if (stretch < 0):
                self.__TowardsX = self.__X
                self.__TowardsY = self.__Y + 1
                self.X = self.__X - self.__MidpointX
                self.Y = self.__Y - self.__MidpointY
                return
            else:
                self.__TowardsX = self.__X
                self.__TowardsY = self.__Y - 1
                self.X = self.__X - self.__MidpointX
                self.Y = self.__Y - self.__MidpointY
                return

        theta = 90 - degrees(atan(self.getSlope()))

        sina = sin(theta)
        cosa = cos(theta)

        pX = tempX - self.__MidpointX
        pY = tempY - self.__MidpointY

        if (stretch >= 0):
            newY = slope * (self.__X + 1 - tempX) + tempY
        else:
            newY = slope * (self.__X - 1 - tempX) + tempY

        self.__TowardsX = (cosa * pX - sina * pY) + tempX
        self.__TowardsY = (sina * pX + cosa * pY) + newY

        self.X = self.__X - self.__MidpointX
        self.Y = self.__Y - self.__MidpointY


    #Gets the current position
    def getPosition(self):
        return self.X, self.Y

    #Gets the current slope
    def getSlope(self):
        if (self.__TowardsX - self.__X == 0):
            return float("inf")
        else:
            return (self.__TowardsY - self.__Y) / (self.__TowardsX - self.__X)

    #gets nearby cells
    def getNearby(self, radius):
        radius *= (int) (1.0 / self.__Scale)
        nearby = []
        for i in xrange(self.__X - radius, self.__X + radius):
            row = []
            for j in xrange(self.__Y - radius, self.__Y + radius):
                try:
                    row.append(self.Plot[i][j]);
                except IndexError:
                    row.append(MemoryTypes.OffGrid)
            nearby.append(row)
        return nearby

    #gets point at position
    def getPointAtPosition(self, x, y):
        return mem.Plot[x + int(self.__MidpointX)][y + int(self.__MidpointY)]

    #Expands the array
    def expandPlot(self, radius):
        topBottom = [MemoryType.Unknown for height in xrange(len(self.Plot))]
        dupe = self.Plot
        self.Plot = []
        for i in xrange(radius):
            self.Plot.append(topBottom)
        for i in xrange(radius - 1, len(dupe)):
            temp = [MemoryType.Unknown for width in xrange(radius)]
            temp.extend(dupe[i])
            temp.extend([MemoryType.Unknown for width in xrange(radius)])
            self.Plot.append(temp)
        for i in xrange(radius):
            self.Plot.append(topBottom)

print ("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
sim = Myro.Simulation("test", 250, 250, Myro.Color("White"))
r = Myro.makeRobot("SimScribbler", sim)
r.setPose(125, 125, -90)
mem = RobotMemory(3, 20, 20, 1, 1, 0, 1)
mem.start(0, 0)