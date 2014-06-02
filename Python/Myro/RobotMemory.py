#-------------------------------------------------------------------------------
<<<<<<< HEAD
# Name:        Robot Memory
# Purpose:     Stores memory about where robot has been
# Author:      Liam McInory
# Created:     06/03/2014
# Copyright:   (c) Liam 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
from __future__ import division
from math import *
=======



# Name:        Robot Memory



# Purpose:     Stores memory about where robot has been



# Author:      Liam McInory



# Created:     06/03/2014



# Copyright:   (c) Liam 2014



# Licence:     MIT



#-------------------------------------------------------------------------------



from __future__ import division

>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197
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

<<<<<<< HEAD
    __Scale = 0.5
=======
    TowardsX = 0

    TowardsY = 0
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197




    #initialize robot, and create memory
    def __init__ (self, comPort = 3, width = 250, height = 250, speed = 0.5, scale = 0.5, lookX = 0, lookY = 1):
<<<<<<< HEAD
        #set global variables
=======

        #set global variables

>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197
        self.Speed = speed
        self.__Scale = scale

        self.__TowardsX = lookX
        self.__TowardsY = lookY

        self.__MidpointX = width / 2
        self.__MidpointY = height / 2

<<<<<<< HEAD
        multiplyBy = (int)(1.0 / scale)
=======
        self.TowardsY = lookY

        self.MidpointX = width / 2

        self.MidpointY = height / 2

        multiplyBy = (int)(1.0 / scale)

        self.Plot = [[0] * width * multiplyBy for col in range(height * multiplyBy)]

        self.MidpointX *= multiplyBy

        self.MidpointY *= multiplyBy
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197

        self.Plot = [[MemoryType.Unknown] * width * multiplyBy for col in range(height * multiplyBy)]

        self.__MidpointX *= multiplyBy
        self.__MidpointY *= multiplyBy

        Myro.init("COM" + str(comPort))

    #Expands the array
    def expandPlot(self, x, y):
        for i in xrange(len(self.Plot)):
            for j in xrange(x * (1 / self.__Scale)):
                self.Plot[i].append(MemoryType.Unknown)
        addArray = self.Plot[0]
        for j in xrange(y):
            self.Plot.append(addArray)



    #set midpoint, and current coordinates
    def start(self, x, y):
        self.__X = x + self.__MidpointX
        self.__Y = y + self.__MidpointY

        self.__TowardsX += self.__MidpointX
        self.__TowardsY += self.__MidpointY

        self.Plot[(int) (floor(self.__X))][(int) (floor(self.__Y))] = 1

<<<<<<< HEAD
        self.X = x
        self.Y = y
=======
        self.Y = y + self.MidpointY

        self.TowardsX += self.MidpointX

        self.TowardsY += self.MidpointY

        self.Plot[(int) (floor(self.X))][(int) (floor(self.Y))] = 1
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197





    #Turn a specified degrees
<<<<<<< HEAD
    def turn(self, degrees):
=======

    def Turn(self, degrees, left):

>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197
        #3 = 1.5s/0.5speed = 90 degrees
        time90 = 3 * abs(self.Speed)
        time = time90 / abs(degrees)

<<<<<<< HEAD
        left = 0
=======


        if (left == 1):
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197

        if (degrees >= 0):
            left = 1

        if (left == 1):
            degrees += 90
            Myro.robot.turnLeft(time, abs(self.Speed))



        else:
            Myro.robot.turnRight(time, abs(self.Speed))

<<<<<<< HEAD
        #get rotation values
        degrees *= (pi / 180)
        sina = sin(degrees)
        cosa = cos(degrees)


        #origin points
        pX = self.__TowardsX - self.__X
        pY = self.__TowardsY - self.__Y
=======


        #get rotation values

        degrees *= (pi / 180)

        sina = sin(degrees)

        cosa = cos(degrees)



        #origin points

        pX = self.TowardsX - self.X

        pY = self.TowardsY - self.Y



        #apply rotation

        self.TowardsX = (cosa * pX - sina * pY) + self.X

        self.TowardsY = (sina * pX + cosa * pY) + self.Y
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197

        #apply rotation
        if (left == 0):
            #reflect across X axis
            self.__TowardsX = -(cosa * pX - sina * pY) + self.__X
            self.__TowardsY = (sina * pX + cosa * pY) + self.__Y
            return

        self.__TowardsX = (cosa * pX - sina * pY) + self.__X
        self.__TowardsY = (sina * pX + cosa * pY) + self.__Y


<<<<<<< HEAD
    #move forward
    def goForward(self, duration):
        #if line is up and down
        if (self.__TowardsX - self.__X == 0):
            #go forward
=======
    def GoForward(self, duration):

        #if line is up and down

        if (self.TowardsX - self.X == 0):

            #go forward

>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197
            Myro.robot.motors(self.Speed, self.Speed)

            Myro.wait(abs(duration))

            Myro.robot.stop()

<<<<<<< HEAD
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
=======


            #get the amount of points forward

            divisible = duration // self.Scale



            #add them to the direction

            self.TowardsY += divisible

            tempY = self.Y



            for y in xrange(self.Y, divisible + tempY):

                if (y % self.Scale == 0):

                    self.Plot[(int) (self.X)][y] = 1
            self.Y += divisible

            return



        #calc slope

        slope = (self.TowardsY - self.Y) / (self.TowardsX - self.X)
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197

        #calc slope
        slope = (self.__TowardsY - self.__Y) / (self.__TowardsX - self.__X)
        tempX = self.__X
        tempY = self.__Y

<<<<<<< HEAD
=======
        tempY = self.Y



>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197
        #go forward
        Myro.robot.motors(self.Speed, self.Speed)
        Myro.wait(abs(duration))

        Myro.robot.stop()


<<<<<<< HEAD
=======

>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197
        #get the amount of points forward
        divisible = duration // self.__Scale

<<<<<<< HEAD
        #add them to the direction
        self.__TowardsX += divisible
        self.__TowardsY += divisible
=======
        divisible = duration / self.Scale



        #add them to the direction

        self.TowardsX += divisible

        self.TowardsY += divisible
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197



        Xs = []
        Ys = []

<<<<<<< HEAD
        if (slope >= 0):
            #positive slope
            for x in xrange(self.__X + self.__Scale, (tempX + divisible) + self.__Scale, self.__Scale):
                #get point
                y = (slope * (x - self.__X)) + self.Y
                #find out if it is a plottable point
                if (y % self.__Scale == 0.0):
                    Xs.append((int)(x))
                    Ys.append((int)(y))
=======


        for x in xrange(self.X, (tempX + divisible)):

            #find out if it is a plottable point

            if (((slope * (x - self.X)) + self.Y) % self.Scale == 0.0):
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197

        else:
            #negative slope
            for x in xrange((tempX - divisible), self.__X, self.__Scale):
                #get point
                y = (slope * (x - self.__X)) + self.Y
                #find out if it is a plottable point
                if (y % self.__Scale == 0.0):
                    Xs.append((int)(x))
                    Ys.append((int)(y))

<<<<<<< HEAD
=======
                Ys.append((int)((slope * (x - self.X)) + self.Y))

>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197
        #Plot the points
        for i in xrange(0, len(Xs)):
            try:
                self.Plot[Xs[i]][Ys[i]] = MemoryType.Visited
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

<<<<<<< HEAD
        if (self.getSlope() != float("nan")):
            theta = (90 * (pi / 180)) - atan(self.getSlope())

            sina = sin(theta)
            cosa = cos(theta)
    
            for i in xrange(0, len(tempXs)):
                pX = self.__TowardsX - tempXs[i]
                pY = self.__TowardsY - tempYs[i]
=======

        self.X = Xs[len(Xs) - 1]

        self.Y = Ys[len(Ys) - 1]



>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197

                tempXs[i] = (cosa * pX - sina * pY) + tempXs[i]
                tempYs[i] = (sina * pX + cosa * pY) + tempYs[i]

                if (tempXs[i] % self.__Scale == 0 and tempYs[i] % self.__Scale == 0):
                    Xs.append(tempXs[i])
                    Ys.append(tempYs[i])
        else:
            for i in xrange(0, len(tempXs)):
                if (tempXs[i] % self.__Scale == 0 and tempYs[i] % self.__Scale == 0):
                    Xs.append(tempXs[i])
                    Ys.append(tempYs[i])

        #Plot the points
        for i in xrange(0, len(Xs)):
            try:
                self.Plot[Xs[i]][Ys[i]] = MemoryType.Visited
            except IndexError:
                print("Error: Ran out of space. Expanding the plot.\r\n")
                self.ExpandPlot(5, 5)
                i -= 1

        multiplyBy = 1.0 / self.__Scale

        if (stretch >= 0):
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

        #add it to the direction TODO: Correct
        self.__TowardsX = maxAmount
        try:
            self.__TowardsY = stretch * (sqrt(1 - pow(((maxAmount - self.__X - stretch) / stretch), 2))) + self.__Y
        except ValueError:
            self.TowardsY = -stretch * (sqrt(1 - pow(((maxAmount - self.__X - stretch) / stretch), 2))) + self.__Y

        self.X = self.__X - self.__MidpointX
        self.Y = self.__Y - self.__MidpointY


    #Gets the current position
    def getPosition(self):
        return [self.X, self.Y]

    #Gets the current slope
    def getSlope(self):
        if (self.__TowardsX - self.__X == 0):
            return float("nan")
        else:
            return (self.__TowardsY - self.__Y) / (self.__TowardsX - self.__X)

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

print ("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
sim = Myro.Simulation("test", 250, 250, Myro.Color("White"))

r = Myro.makeRobot("SimScribbler", sim)

r.setPose(125, 125, -90)
<<<<<<< HEAD
mem = RobotMemory(3, 20, 20, 1, 1, 1, 1)
mem.start(0, 0)
mem.curve(.5, .5, 6)
print(mem.Plot)
=======

mem = RobotMemory(3, 20, 20, 1, 1, 0, 1)

mem.Start(0, 0)

mem.GoForward(2)

mem.Turn(-45, 1)

mem.GoForward(3)

print (mem.Plot[::-1])
>>>>>>> fad097be7a9f972463c8f13ce5a3c37b8f515197
