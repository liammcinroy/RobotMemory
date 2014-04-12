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

MemoryTypes = enum(Unknown=0, Visited=1) #add more if you want


class RobotMemory:

    Plot = [[]]

    X = 0
    Y = 0

    __MidpointX = 0
    __MidpointY = 0

    __X = 0
    __Y = 0

    __TowardsX = 0
    __TowardsY = 0

    __Scale = 0.0


    #initialize robot, and create memory
    def __init__ (self, comPort = 3, width = 250, height = 250, speed = 0.5, scale = 0.5, lookX = 0, lookY = 1):
        #set global variables
        self.Speed = speed
        self.__Scale = scale

        self.__TowardsX = lookX
        self.__TowardsY = lookY

        self.__MidpointX = width / 2
        self.__MidpointY = height / 2

        multiplyBy = (int)(1.0 / scale)

        self.Plot = [[MemoryTypes.Unknown] * width * multiplyBy for col in range(height * multiplyBy)]

        self.__MidpointX *= multiplyBy
        self.__MidpointY *= multiplyBy

        Myro.init("COM" + str(comPort))

    #Expands the array
    def ExpandPlot(self, x, y):
        for i in xrange(len(self.Plot)):
            for j in xrange(x * (1 / self.__Scale)):
                self.Plot[i].append(MemoryTypes.Unknown)
        addArray = self.Plot[0]
        for j in xrange(y):
            self.Plot.append(addArray)

    #set midpoint, and current coordinates
    def Start(self, x, y):
        self.__X = x + self.__MidpointX
        self.__Y = y + self.__MidpointY

        self.__TowardsX += self.__MidpointX
        self.__TowardsY += self.__MidpointY

        self.Plot[(int) (floor(self.__X))][(int) (floor(self.__Y))] = 1

        self.X = x
        self.Y = y



    #Turn a specified degrees
    def Turn(self, degrees):
        #3 = 1.5s/0.5speed = 90 degrees
        time90 = 3 * abs(self.Speed)
        time = time90 / abs(degrees)

        left = 0

        if (degrees >= 0):
            left = 1

        if (left == 1):
            degrees += 90
            Myro.robot.turnLeft(time, abs(self.Speed))

        else:
            Myro.robot.turnRight(time, abs(self.Speed))

        #get rotation values
        degrees *= (pi / 180)
        sina = sin(degrees)
        cosa = cos(degrees)


        #origin points
        pX = self.__TowardsX - self.__X
        pY = self.__TowardsY - self.__Y

        #apply rotation
        if (left == 0):
            #reflect across X axis
            self.__TowardsX = -(cosa * pX - sina * pY) + self.__X
            self.__TowardsY = (sina * pX + cosa * pY) + self.__Y
            return

        self.__TowardsX = (cosa * pX - sina * pY) + self.__X
        self.__TowardsY = (sina * pX + cosa * pY) + self.__Y


    #move forward
    def GoForward(self, duration):
        #if line is up and down
        if (self.__TowardsX - self.__X == 0):
            #go forward
            Myro.robot.motors(self.Speed, self.Speed)
            Myro.wait(abs(duration))
            Myro.robot.stop()

            #get the amount of points forward
            divisible = duration // self.__Scale

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
                        self.ExpandPlot(0, 5)
                        y -= 1

            #increase y
            self.__Y += divisible
            self.Y += divisible
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

        Xs = []
        Ys = []

        if (slope >= 0):
            #positive slope
            for x in xrange(self.__X + self.__Scale, (tempX + divisible) + self.__Scale):
                #find out if it is a plottable point
                if (((slope * (x - self.__X)) + self.__Y) % self.__Scale == 0.0):
                    Xs.append(x)
                    Ys.append((int)((slope * (x - self.__X)) + self.__Y))

        else:
            #negative slope
            for x in xrange((tempX - divisible), self.__X):
                #find out if it is a plottable point
                if (((slope * (x - self.__X)) + self.__Y) % self.__Scale == 0.0):
                    Xs.append(x)
                    Ys.append((int)((slope * (x - self.__X)) + self.__Y))

        #Plot the points
        for i in xrange(0, len(Xs)):
            try:
                self.Plot[Xs[i]][Ys[i]] = MemoryTypes.Visited
            except IndexError:
                print("Error: Ran out of space. Expanding the plot.\r\n")
                self.ExpandPlot(5, 5)
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

    #Gets the current position
    def GetPosition(self):
        return [self.X, self.Y]

    #Gets the current slope
    def GetSlope(self):
        if (self.__TowardsX - self.__X == 0):
            return float("nan")
        else:
            return (self.__TowardsY - self.__Y) / (self.__TowardsX - self.__X)