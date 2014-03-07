#-------------------------------------------------------------------------------

# Name:        Robot Memory

# Purpose:     Stores memory about where robot has been

#

# Author:      Liam McInory

#

# Created:     06/03/2014

# Copyright:   (c) Liam 2014

# Licence:     MIT

#-------------------------------------------------------------------------------

import Myro

from math import *



class RobotMemory:

    Plot = [[]]

    Speed = 0.0

    MidpointX = 0

    MidpointY = 0

    X = 0

    Y = 0

    TowardsX = 0

    TowardsY = 0

    Scale = 0.0

    def __init__ (com = 3, length = 250, height = 250, speed = 0.5, scale = 0.5, lookX = 0, lookY = 1):

        Plot = [[0 for x in xrange(length)] for x in xrange(height)]

        Speed = speed

        Scale = scale

        TowardsX = lookX

        TowardsY = lookY

        #Myro.init("COM" + com)


    def Start(x, y):

        MidpointX = x

        MidpointY = y

        X = MidpointX

        Y = MidpointY



    def Turn(degrees, left):

        time90 = 3 * abs(Speed)

        time = Time90 / abs(degrees)

        if (left == 1):

            Myro.robot.turnLeft(time, abs(Speed))

        else:

            Myro.robot.turnRight(time, abs(Speed))

        TowardsX = TowardsX * cos(degrees) + TowardsY * sin(degrees)

        TowardsY = TowardsX * -sin(degrees) + TowardsY * sin(degrees)



    def GoForward(duration):

        slope = (TowardsY - Y) / (TowardsX - X)

        tempX = X

        tempY = Y

        TowardsX += duration

        TowardsY += duration

        Myro.robot.motors(Speed, Speed)

        wait(duration)

        divisible = duration / Scale

        Xs = []

        Ys = []

        for x in xrange(X, divisible):

            if (slope * x + X % Scale == 0):

                Xs.append(x)

                Ys.append(slope * x + X)

        for x in xrange(len(Xs)):

            for y in xrange(len(Ys)):

                if (Plot[Xs[x]][Ys[y]] == 0):

                    Plot[Xs[x]][Ys[y]] = 1

        X += divisible

        Y += divisible



sim = Myro.Simulation("test", 250, 250, Myro.Color("White"))
r = Myro.makeRobot("SimScribbler", sim)
r.setPose(125, 125, -90)
mem = RobotMemory()
mem.Start(125, 125)
mem.GoForward(1)
