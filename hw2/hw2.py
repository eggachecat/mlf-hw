import numpy as np
import pylab as pl

import logging

logging.basicConfig(level=logging.INFO)

# return sorted (x, y)
def generateData(size):

	x = np.random.uniform(-1, 1, size = size)
	logging.debug("ini x = %s", (str(x)))
	# sign(x)
	s = x > 0
	logging.debug(" s(x) = %s", (str(s)))
	# 20% error
	noise = np.random.choice([True, False, False, False, False], size = size)
	logging.debug("noise = %s", (str(noise)))
	# X xor True = not X ; X xor False = X;
	y = 2 * np.logical_xor(s, noise) - 1
	logging.debug("y = s(x) # noise = %s", (str(y)))

	return x, y

def loadData(filename):

	dataset = np.loadtxt(filename)

	t_dataset = np.transpose(dataset)

	y = t_dataset[-1]
	xMatrix = np.transpose(t_dataset[:-1])

	return xMatrix, y


class DSA():

	def __init__(self, direction, theta, dim = 1):

		self.direction = direction
		self.theta = theta
		self.dim = dim



	def predict1d(self, x):
		return self.direction * (2 * (x > self.theta) - 1)

	def predict(self, x, dim):
		return self.predict1d(x[dim])

	def calculateError(self, x, y):

		err = 0
		for i in range(0, x.size):
			if not y[i] == self.predict1d(x[i]):
				err += 1
		self.Ein = err / x.size
		return err

	def drawDecision(self, x, xRange = [-1,1]):

		pl.xlim(xRange)

		pl.plot(self.theta, 0.5, "g^")

		for i in range(0, x.size):
			if self.predict1d(x[i]) == 1:
				symbol = "bs"
			else:
				symbol = "ro"
			pl.plot(x[i], 0.5, symbol)
		pl.show()

	def getEout(self):
		return 0.5 + 0.3 * self.direction * (np.absolute(self.theta) - 1)

	def getEin(self):
		return self.Ein



	@staticmethod
	def cleanData(x, y):
		pass


	@staticmethod 
	# make sure x and y are both np.array
	def learn1d(x, y):

		sortIndexArr = np.argsort(x)
		x = x[sortIndexArr]
		y = y[sortIndexArr]

		negBorder = x[0] - 1
		posBorder = x[-1] + 1

		# make sure dataset splits line into N+1 areas
		dichotomies = np.insert(x, 0, negBorder)
		dichotomies = np.append(dichotomies, posBorder)
		# let theta be the center of two values
		dichotomies = (dichotomies + np.roll(dichotomies, -1)) / 2
		dichotomies = np.delete(dichotomies, -1)
		logging.debug("dichotomies are %s", (str(dichotomies)))

		minErr = float('inf')
		g = None

		for direction in [-1, 1]:
			for theta in  dichotomies:

				dsa = DSA(direction, theta)
				err = dsa.calculateError(x, y)

				if err < minErr:
					minErr = err
					g = dsa

				del dsa

				logging.debug("err is: %f with direction = %d, theta = %f" % (err, direction, theta))
		logging.debug("min-err is: %f" % (minErr))
		
		return g

	@staticmethod 
	def learn(xMatrix, y):

		t_xMatrix = np.transpose(xMatrix)

		dim = t_xMatrix.shape[0]
		pl.figure(0, figsize=(14.0, 10.0))
		pl.ylim([-1, dim])

		minErr = float('inf')
		bestH = None
		bestI = 0

		for i in range(0, dim):
			x = np.transpose(t_xMatrix[i])

			DSA.draw(x, y, i)

			g = DSA.learn1d(x, y)
			err = g.getEin()

			logging.info("at dim %d, err is: %f with direction = %d, theta = %f" % (i, err, g.direction, g.theta))

			if err < minErr:
				minErr = err
				bestH = g
				bestI = i
				logging.info("update dim %d as the optimal dim" % (i))
			del g

		DSA.saveAndCloseFigure(("%s/%s.png") % ("all_output", "Q19"), "Data distribution in different dimension", "real-value", "dimension")

		return bestH, bestI

	@staticmethod
	def saveAndCloseFigure(dstPath, title = "", xlabel= "", ylabel= ""):
		pl.title(title)
		pl.xlabel(xlabel)
		pl.ylabel(ylabel)
		pl.savefig(dstPath)
		pl.close()

	@staticmethod
	def draw(x, y, dim = 0):

		for i in range(0, y.size):
			if y[i] == 1:
				symbol = "bs"
			else:
				symbol = "ro"
			pl.plot(x[i], dim, symbol)


def hw2_17_18():
		
	total_times = 5000
	cumEin = 0
	cumEout = 0
	EinArr = []
	EoutArr = []

	for t in range(0, total_times):

		x, y = generateData(20)

		g = DSA.learn1d(x, y)
		EinArr.append(g.getEin())
		EoutArr.append(g.getEout())

	print("average Ein = %f, average Eout = %f" % (np.mean(EinArr), np.mean(EoutArr)))

	pl.hist(EinArr, bins='auto')
	DSA.saveAndCloseFigure(("%s/%s.png") % ("all_output", "Q17"), "E_in Histogrom", "err_rate", "frequency")

	pl.hist(EoutArr, bins='auto')
	DSA.saveAndCloseFigure(("%s/%s.png") % ("all_output", "Q18"), "E_out Histogrom", "err_rate", "frequency")



def hw2_19_20():

	train_xMatrix, train_y = loadData("./data/hw2_train.dat")
	g, dim = DSA.learn(train_xMatrix, train_y)

	print("The optimal decision stump is the one with s = %d and theta = %f at dimension %d whose Ein = %f" % (g.direction, g.theta, dim, g.getEin()))

	EoutCtr = 0
	test_xMatrix, test_y = loadData("./data/hw2_test.dat")
	datasetSize = test_xMatrix.shape[0]
	for i in range(0, datasetSize):
		x = test_xMatrix[i]
		EoutCtr += int(not g.predict(x, dim) == test_y[i])

	print("Havig run the optimal decision stump on test dataset, we got %d errors in total %d tries, E_test = %f " % (EoutCtr, datasetSize, EoutCtr / datasetSize))



hw2_17_18()
hw2_19_20()
