import numpy as np
import hw1pla
import hw1pocket



def pla_exp(dataPairs, alpha, random, countUpdates):


	dim = len(dataPairs[0]["input"])

	solution = hw1pla.PLA({"dim": dim, "alpha": alpha})

	halt = False
	updateCtr = 0

	seq = range(0, len(dataPairs))
	if random:
		seq = np.random.permutation(seq)

	if countUpdates:
		indexUpdateCtr = dict()

	while not halt:
		halt = True

		for i in seq:
			correct = solution.train(dataPairs[i])
			halt = halt and correct
			updateCtr += int(not correct)

			if countUpdates and not correct:
				if not i in indexUpdateCtr:
					indexUpdateCtr[i] = 0
				indexUpdateCtr[i] += 1


	if countUpdates:
		print(indexUpdateCtr)
		maxValue = max(list(indexUpdateCtr.values()))
		print(maxValue)

		for index, value in indexUpdateCtr.items():
			if value == maxValue:
				print("The index that results in the most number of update is %d" % (index))

	# print("updateCtr = %d when pla halted" %(updateCtr, solution.test(dataPairs)))
	return str(solution.weight), updateCtr


def pocket_exp(trainingDataPairs, testDataPairs, alpha, maxUpdate, usePocketWeight):

	trainingDim = len(trainingDataPairs[0]["input"])
	testDim = len(testDataPairs[0]["input"])

	if not testDim == trainingDim:
		print("dim of test-data-input should equal to training-data-input")
		exit()

	solution = hw1pocket.PocketPLA({"dim": trainingDim, "alpha": alpha})


	updateCtr = 0
	totalDataNum = len(trainingDataPairs)

	while True:
		i = np.random.randint(totalDataNum)

		correct = solution.train(trainingDataPairs[i], trainingDataPairs)
		updateCtr += int(not correct)

		if updateCtr == maxUpdate:
			break;
			
	if usePocketWeight:
		solution.weight = solution.pocketWeight

	errors = solution.test(testDataPairs)

	return str(solution.weight), errors / totalDataNum
