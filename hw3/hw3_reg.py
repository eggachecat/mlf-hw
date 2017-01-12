import numpy as np
import pylab as pl
import os

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


def loadData(dataPath):

	dataset = np.loadtxt(dataPath)

	t_dataset = np.transpose(dataset)

	y = t_dataset[-1]


	# print((t_dataset[:-1]))
	xMatrix = np.transpose(t_dataset[:-1])

	return xMatrix, y

class RegularizedLinerRegression():

	def __init__(self, config):
		
		self._lambda = config["lambda"]
		self.weight = None

	def train(self, xMatrix, y):

		dim = np.shape(xMatrix)[1]
		m_lambda = self._lambda * np.identity(dim)
		# come from problem 10 
		self.weight = np.dot(np.linalg.inv(np.dot(np.transpose(xMatrix), xMatrix) + m_lambda), np.dot(np.transpose(xMatrix), y))

	def test(self, testSet):

		errCtr = 0
		for pair in testSet:
			y = pair["truth"]
			x = np.insert(pair["input"], 0, np.array((1)), 0)

			s = np.dot(np.transpose(self.weight), x)

			l = 1 if s > 0 else -1

			if not l == y:
				errCtr += 1

		return errCtr / len(testSet)

def exp(_lambda):
	xMatrix, y = loadData("./data/hw4_train.dat")
	xMatrix = np.insert(xMatrix, 0, np.array((1)), 1)


	rl = RegularizedLinerRegression({
			"lambda": _lambda
		})
	rl.train(xMatrix, y)

	EinTestSet, dim = makePairs("./data/hw4_train.dat")
	Ein = rl.test(EinTestSet)
	

	EoutTestSet, dim = makePairs("./data/hw4_test.dat")
	Eout = rl.test(EoutTestSet)
	print("lambda=", np.log10(_lambda), "Ein = ", Ein, "Eout = ", Eout)

	return Ein, Eout



def exp_split(_lambda, splitIndex = 120):


	xMatrix, y = loadData("./data/hw4_train.dat")
	xMatrix = np.insert(xMatrix, 0, np.array((1)), 1)


	xMatrixTrain = xMatrix[:splitIndex]
	yTrain = y[:splitIndex]


	rl = RegularizedLinerRegression({
			"lambda": _lambda
		})
	rl.train(xMatrixTrain, yTrain)

	trainingSet, dim = makePairs("./data/hw4_train.dat")
	Etrain = rl.test(trainingSet[:splitIndex])
	Evalid = rl.test(trainingSet[splitIndex:])

	EoutTestSet, dim = makePairs("./data/hw4_test.dat")
	Eout = rl.test(EoutTestSet)

	# print("lambda=", np.log10(_lambda), "Etrain = ", Etrain, "Evalid = ", Evalid, "Eout = ", Eout)
	print( Etrain, Evalid, Eout)


	return Etrain, Evalid, Eout


def exp_test_lambda(exp_method, errIndex, title):

	log10_lambda_list = range(-10,3)
	ErrExpRecords = []

	minErr = float("inf")
	gLambda = 0
	for log10_lambda in log10_lambda_list:

		# print("lambda = ",log10_lambda)
		_lambda = 10 ** log10_lambda
		err = exp_method(_lambda)[errIndex]
		if not minErr < err:
			minErr = err
			gLambda = _lambda

		ErrExpRecords.append(err)

	pl.plot(log10_lambda_list, ErrExpRecords)
	pl.xlim([-11,3])
	pl.ylim([min(ErrExpRecords)-0.01, max(ErrExpRecords)+0.01])
	pl.xlabel(r"$log_{10}\lambda$")
	pl.ylabel("Error")
	pl.title(title)
	pl.plot(log10_lambda_list, ErrExpRecords,'rs');

def exp_cross_valid(_lambda):

	
	xMatrix, y = loadData("./data/hw4_train.dat")
	xMatrix = np.insert(xMatrix, 0, np.array((1)), 1)

	testSet, dim = makePairs("./data/hw4_train.dat")
	# Etrain = rl.test(trainingSet[:splitIndex])
	# Evalid = rl.test(trainingSet[splitIndex:])


	folds = []

	# x is the cv-fold
	for x in range(0,5):

		keyArr = range(x * 40, x * 40 + 40)
		rl = RegularizedLinerRegression({"lambda": _lambda})
		xMatrixTrain = np.delete(xMatrix, keyArr, 0)
		yTrain = np.delete(y, keyArr, 0)

		rl.train(xMatrixTrain, yTrain)
				
		folds.append(rl.test(testSet[x * 40 : x * 40 + 40]))


	# print("lambda=", np.log10(_lambda), "Ecv = ", sum(folds) / len(folds))
	print(np.log10(_lambda), sum(folds) / len(folds))


	return [sum(folds) / len(folds)]

def saveFigure(filename):
	if not os.path.exists("all_output"):
		os.makedirs("all_output")
	pl.savefig("all_output/%s.png" % (filename))
	pl.close()


def exp_16_17(errIndex, title):
	exp_test_lambda(exp_split, errIndex, title)


# errIndex = 0 <=> Ein
def exp_14_15(errIndex, title):
	exp_test_lambda(exp, errIndex, title)
	


def problem_13():
	exp(1.126)

def problem_14():
	exp_14_15(0, r"$E_{in}$ versus $log_{10}\lambda$")
	saveFigure("problem_14")

def problem_15():
	exp_14_15(1, r"$E_{out}$ versus $log_{10}\lambda$")
	saveFigure("problem_15")
	
def problem_16():
	exp_16_17(0, r"$E_{train}$ versus $log_{10}\lambda$")
	saveFigure("problem_16")

def problem_17():
	exp_16_17(1, r"$E_{valid}$ versus $log_{10}\lambda$")
	saveFigure("problem_17")

def problem_18():
	# lambda = 1 comes from problem_17
	exp(1)

def problem_19():
	# lambda = 1 comes from problem_17
	exp_test_lambda(exp_cross_valid, 0, r"$E_{cv}$ versus $log_{10}\lambda$")
	saveFigure("problem_19")
	
def problem_20():
	# lambda = 1e-8 comes from problem_19
	exp(1e-8)


problem_13()
problem_14()
problem_15()
problem_16()
problem_17()
problem_18()
problem_19()
problem_20()