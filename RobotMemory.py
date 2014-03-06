#-------------------------------------------------------------------------------
# Name:        Robot Memory
# Purpose:     Stores memory about where robot has been
#
# Author:      Liam McInory
#
# Created:     06/03/2014
# Copyright:   (c) Liam 2014
# Licence:     GNU
#-------------------------------------------------------------------------------
from Myro import *
from math import *

class RobotMemory:
    Plot = [[]]
    Speed = 0.0
    MidpointX = 0
    MidpointY = 0
    Robot = 0
    X = 0
    Y = 0
    TowardsX = 0
    TowardsY = 0
    Scale = 0.0
    def __init__ (robot, length, height, speed = 0.5, scale = 0.5, lookX = 0, lookY = 1):
        Plot = [[0 for x in xrange(length)] for x in xrange(height)]
        Speed = speed
        Robot = robot
        Scale = scale
        X = MidpointX
        Y = MidpointY
        TowardsX = lookX
        TowardsY = lookY

    def Start(x, y):
        MidpointX = x
        MidpointY = y
        X = MidpointX
        Y = MidpointY

    def Turn(degrees, left):
        time90 = 3 * abs(Speed)
        time = Time90 / abs(degrees)
        if (left == 1):
            Robot.turnLeft(time, abs(Speed))
        else:
            Robot.turnRight(time, abs(Speed))
        TowardsX = TowardsX * cos(degrees) + TowardsY * sin(degrees)
        TowardsY = TowardsX * -sin(degrees) + TowardsY * sin(degrees)

    def GoForward(duration):
        slope = (TowardsY - Y) / (TowardsX - X)
        TowardsX += duration
        TowardsY += duration
        Robot.motors(Speed, Speed)
        wait(duration)
        divisible = duration / Scale
        for x in xrange(X, divisible):
            for y in xrange(Y, divisible):
                if (Plot[x][y] == 0):
                    Plot[x][y] = 1
        X += divisible
        Y += divisible

