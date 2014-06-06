from random import randint

array = [[randint(0, 10)] * 10 for height in xrange(10)]

array[0] = randint(0, 10)

print(array)