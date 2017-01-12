import numpy as np
import pylab as pl

def sign(x):
	return 2 * (x > 0) - 1

def keep(x):
	return x

# x can be real while divisor should be integer
def realMod(x, divisor):

	quotient = np.floor(x / divisor)

	return x - quotient * divisor



# triangle-wave
def tw(x, alpha):
	return sign(np.absolute(realMod(alpha * x, 4) - 2) - 1)


def devil(x, y):

	c = 1 + x + y
	return np.power(c, x) + np.power(c, y) - np.power(2, c)


def f(N):
	return np.power(N,3) + np.power(N,5) - np.power(2,N)


xRange = np.arange(-5,5,0.1)
alpha = 1

yRange = [tw(x, alpha) for x in xRange]

pl.plot(xRange, yRange)
pl.show()