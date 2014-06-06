from random import randint

array2 = [[randint(0, 10)] * 10 for height in xrange(10)]

def add(array, radius):
    topBottom = [randint(0, 10) for height in xrange(10)]
    dupe = array
    array = []
    for i in xrange(radius):
        array.append(topBottom)
    for i in xrange(radius - 1, len(dupe)):
        temp = [randint(0, 10) for width in xrange(radius)]
        temp.extend(dupe[i])
        temp.extend([randint(0, 10) for width in xrange(radius)])
        array.append(temp)
    for i in xrange(radius):
        array.append(topBottom)
    return array
print(add(array2, 2))