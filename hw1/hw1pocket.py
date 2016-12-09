import hw1pla
import numpy as np

class PocketPLA(hw1pla.PLA):

	def __init__(self, config):

		hw1pla.PLA.__init__(self, config)

		self.pocketWeight = self.weight
		self.errors = np.inf


	def train(self, trainPair, testDataset):

		correct = super(PocketPLA, self).train(trainPair)

		errors = self.test(testDataset)

		if errors < self.errors:
			self.errors = errors
			self.pocketWeight = np.copy(self.weight)
			# print(self.errors)

		return correct