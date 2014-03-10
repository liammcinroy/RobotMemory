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

from __future__ import division

import Myro

from math import *


class RobotMemory:

    Plot = [[]]

    MidpointX = 0

    MidpointY = 0

    X = 0

    Y = 0

    TowardsX = 0
    
    TowardsY = 0

    Scale = 0.0

    #initialize robot, and create memory

    def __init__ (self, comPort = 3, width = 250, height = 250, speed = 0.5, scale = 0.5, lookX = 0, lookY = 1):

        self.Speed = speed

        self.Scale = scale

        self.TowardsX = lookX

        self.TowardsY = lookY
        
        self.MidpointX = width / 2
        
        self.MidpointY = height / 2
        
        multiplyBy = (int)(1.0 / scale)
        
        self.Plot = [[0] * width * multiplyBy for col in range(height * multiplyBy)]
        
        self.MidpointX *= multiplyBy
        
        self.MidpointY *= multiplyBy
        

        #Myro.init("COM" + comPort)

    #set midpoint, and current coordinates

    def Start(self, x, y):

        self.X = x + self.MidpointX

        self.Y = y + self.MidpointY
        
        self.TowardsX += self.MidpointX
        
        self.TowardsY += self.MidpointY
        
        self.Plot[(int) (floor(self.X))][(int) (floor(self.Y))] = 1


    #Turn a specified degrees

    def Turn(self, degrees, left):
        
        #3 = 1.5s/0.5speed = 90 degrees

        time90 = 3 * abs(self.Speed)

        time = time90 / abs(degrees)

        if (left == 1):

            Myro.robot.turnLeft(time, abs(self.Speed))

        else:

            Myro.robot.turnRight(time, abs(self.Speed))
            
        #apply rotation matrix

        self.TowardsX = self.TowardsX * cos(degrees) + self.TowardsY * sin(degrees)

        self.TowardsY = self.TowardsX * -sin(degrees) + self.TowardsY * sin(degrees)



    def GoForward(self, duration):
        
        if (self.TowardsX - self.X == 0):
            
            Myro.robot.motors(self.Speed, self.Speed)
            
            Myro.wait(abs(duration))
            
            Myro.robot.stop()
            
            #get the amount of points forward
            
            divisible = duration // self.Scale
            
            #add them to the direction
            
            self.TowardsY += divisible
            
            tempY = self.Y
            
            for y in xrange(self.Y, divisible + tempY):
                
                if (y % self.Scale == 0):
                    
                    self.Plot[(int) (self.X)][y] = 1
                    
            return
        
        #calc slope

        slope = (self.TowardsY - self.Y) / (self.TowardsX - self.X)

        tempX = self.X

        tempY = self.Y
        
        #go forward

        Myro.robot.motors(self.Speed, self.Speed)

        Myro.wait(abs(duration))
        
        Myro.robot.stop()
        
        #get the amount of points forward

        divisible = duration / self.Scale
        
        #add them to the direction
        
        self.TowardsX += divisible
        
        self.TowardsY += divisible

        Xs = []

        Ys = []

        for x in xrange(self.X, tempX + divisible):
            #find out if it is a plottable point

            if (((slope * (x - self.X)) + self.Y) % self.Scale == 0.0):

                Xs.append(x)

                Ys.append((int)((slope * (x - self.X)) + self.Y))
        #Plot the points

        for i in xrange(0, len(Xs)):

            if (self.Plot[Xs[i]][Ys[i]] == 0):

                self.Plot[Xs[i]][Ys[i]] = 1

        self.X += divisible

        self.Y += divisible


print ("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

sim = Myro.Simulation("test", 25, 25, Myro.Color("White"))

r = Myro.makeRobot("SimScribbler", sim)

r.setPose(12, 12, -90)

mem = RobotMemory(3, 5, 5, 0.5, 0.5, 1, 1)

mem.Start(0, 0)

mem.GoForward(2)

mem.Turn(-45, 1)

mem.GoForward(2)

print (mem.Plot)
