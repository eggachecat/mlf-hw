import numpy as np
import pylab as pl

class PLA():

	def __init__(self, config):

		# addition one for bais
		self.dim = config["dim"] + 1
		self.alpha = config.get("alpha", 1)
		self.weight = np.zeros((self.dim, 1), dtype=np.float)

	def activate(self, x):
		# sign function
		return (-1 if x < 0 else 1)

	def forward(self, dataInput):

	
		weightedValue = np.dot(
					np.transpose(self.weight), dataInput)

	
		return  self.activate(weightedValue[0,0])

	def update(self, direction, step):
		self.weight += self.alpha * direction * step

	def train(self, trainPair):
		

		dataInput = np.transpose(np.matrix(np.insert(trainPair["input"], 0, 1)))
		truth =  trainPair["truth"]

		predict = self.forward(dataInput)

		correct = predict == truth


		if not correct:
			self.update(truth, dataInput)

		return correct

	def test(self, dataPairs):
		errCtr = 0
		for pair in dataPairs:
			dataInput = np.transpose(np.matrix(np.insert(pair["input"], 0, 1)))
			truth =  pair["truth"]

			predict = self.forward(dataInput)

			if not predict == truth:
				errCtr += 1

		return errCtr

