import numpy as np


def makePairs(dataPath):

	dataset = np.loadtxt(dataPath)

	pairs = []
	for row in dataset:
		splitIndex = len(row) - 1
		pairs.append({
			"input": np.transpose(np.matrix(np.matrix(row[0:splitIndex]))),
			"truth": row[splitIndex]
		})
	return pairs, len(pairs[0]["input"])





def sigmoid(x, c = -1):
	return 1 / (1 + np.exp(c * x))

class LogisticRegression():
	"""docstring for LogisticRegression"""
	def __init__(self, config):
		self.dim = config["dim"]
		self.learningRate = config["eta"]

		# extro 1 for bias
		self.weight = np.zeros((self.dim + 1, 1), dtype=np.float)

	@staticmethod
	def activate(x):
		return sigmoid(x)



	def trainByBatchGradient(self, trainingSet):


		deltaWeight = np.zeros((self.dim + 1, 1), dtype=np.float)
		N = len(trainingSet)

		for pair in trainingSet:

			y = pair["truth"]
			x =  np.insert(pair["input"], 0, np.array((1)), 0)
			o, s = self.predict(x)

			deltaWeight = deltaWeight + sigmoid(-y*s) * (-y*x)

		self.weight = self.weight - (1 / N) * self.learningRate * deltaWeight




	def trainByStochasticGradient(self, pair):


		y = pair["truth"]
		x =  np.insert(pair["input"], 0, np.array((1)), 0)
		o, s = self.predict(x)

		deltaWeight = sigmoid(-y*s) * (-y*x)
		self.weight = self.weight - self.learningRate * deltaWeight


		

	def test(self, testSet):

		errCtr = 0

		for pair in testSet:

			y = pair["truth"]
			x =  np.insert(pair["input"], 0, np.array((1)), 0)

			o, s = self.predict(x)
			l = 1 if s > 0 else -1

			if not l == y:
				errCtr += 1

		return errCtr / len(testSet)

	def predict(self, input):

		score = np.dot(np.transpose(self.weight), input)
		return LogisticRegression.activate(score)[0,0], score[0,0]



trainingSet, dim = makePairs("./data/hw3_train.dat")
testSet, dim = makePairs("./data/hw3_test.dat")
T = 2000




def problem_11(eta):


	lg = LogisticRegression({
		"dim": dim,
		"eta": eta
	})

	for x in range(0,T):
		lg.trainByBatchGradient(trainingSet)
		if (x + 1) % 100 == 0:
			print("Alg has finished %d-time iteration" %(x + 1))
	print(lg.weight)
	print(lg.test(testSet))

def problem_12(eta):

	lg = LogisticRegression({
		"dim": dim,
		"eta": eta
	})

	for x in range(0,T):
		i = x % len(trainingSet)
		lg.trainByStochasticGradient(trainingSet[i])
		if (x + 1) % 100 == 0:
			print("Alg has finished %d-time iteration" %(x + 1))
	print(lg.weight)
	print(lg.test(testSet))


problem_11(0.001)
problem_12(0.001)

