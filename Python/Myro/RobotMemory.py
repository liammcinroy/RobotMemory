#-------------------------------------------------------------------------------



# Name:        Robot Memory



# Purpose:     Stores memory about where robot has been



# Author:      Liam McInory



# Created:     06/03/2014



# Copyright:   (c) Liam 2014



# Licence:     MIT



#-------------------------------------------------------------------------------



from __future__ import division

import Myro

from math import *



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

        self.Plot = [[0] * width * multiplyBy for col in range(height * multiplyBy)]

        self.__MidpointX *= multiplyBy

        self.__MidpointY *= multiplyBy

        #Myro.init("COM" + comPort)


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


            for y in xrange(self.__Y, divisible + tempY):

                if (y % self.__Scale == 0):

                    self.Plot[(int) (self.__X)][y] = 1

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

            for x in xrange(self.__X, (tempX + divisible)):

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

                self.Plot[Xs[i]][Ys[i]] = 1


        diffX = Xs[len(Xs) - 1] - self.__X

        diffY = Ys[len(Ys) - 1] - self.__X

        multiplyBy = 1.0 / self.__Scale

        self.__X = Xs[len(Xs) - 1]

        self.__Y = Ys[len(Ys) - 1]

        self.X += diffX * multiplyBy

        self.Y += diffY * multiplyBy


    def GetPosition(self):

        return [self.X, self.Y]


    def GetSlope(self):

        if (self.__TowardsX - self.__X == 0):

            return float("nan")

        else:

            return (self.__TowardsY - self.__Y) / (self.__TowardsX - self.__X)



print ("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

sim = Myro.Simulation("test", 250, 250, Myro.Color("White"))

r = Myro.makeRobot("SimScribbler", sim)

r.setPose(125, 125, -90)

mem = RobotMemory(3, 20, 20, 1, 1, 0, 1)

mem.Start(0, 0)

print (mem.GetPosition())

mem.GoForward(2)

print (mem.GetPosition())

mem.Turn(-45)

mem.GoForward(3)

print (mem.GetPosition())

print (mem.Plot[::-1])