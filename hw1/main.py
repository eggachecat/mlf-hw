import numpy as np
import pylab as pl
import sqlite3
import os
import time


global __conn, __cursor

def iniGeneralSQLite(dbPath):

	global __conn, __cursor

	newDB = False
	if not os.path.isfile(dbPath):
		newDB = True
	
	__conn = sqlite3.connect(dbPath)
	__conn.row_factory = sqlite3.Row
	__cursor = __conn.cursor()

	if newDB:
		createExpTable()


def createExpTable():

	global __cursor
	__cursor.execute('''CREATE TABLE exp_record
			            (exp_id INTEGER PRIMARY KEY NOT NULL, 
			            perception_structure TEXT, halt_number INTEGER, alpha INTEGER, 
			            exp_info TEXT)''')

def saveExp(perception_structure, halt_number, alpha, exp_info):
	global __conn, __cursor
	
	__cursor.execute('''INSERT INTO exp_record(perception_structure, halt_number, alpha, exp_info)
				 VALUES(?, ?, ?, ?)''', (perception_structure, halt_number, alpha, exp_info))

	# __conn.commit()

def closeDB():
	global __conn
	__conn.commit()
	__conn.close()

"""Perception-Learning-Algorithm"""
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

		# print(dataInput)
		# print(np.transpose(self.weight))

		weightedValue = np.dot(
					np.transpose(self.weight), dataInput)

		# print(weightedValue, self.activate(weightedValue[0,0]))
	
		return  self.activate(weightedValue[0,0])

	def update(self, direction, step):
		self.weight += self.alpha * direction * step

	def train(self, trainPair):
		

		dataInput = np.transpose(np.matrix(np.insert(trainPair["input"], 0, 1)))
		truth =  trainPair["truth"]

		predict = self.forward(dataInput)

		correct = predict == truth

		# print("(%d, %d, %s)"%(predict, truth, correct))

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

	@staticmethod
	def makePairs(dataset):

		pairs = []
		for row in dataset:
			splitIndex = len(row) - 1
			pairs.append({
				"input": row[0:splitIndex],
				"truth": row[splitIndex]
			})

		return splitIndex, pairs

# def exp(dataPairs, solution):
	
# 	halt = False
# 	ctr = 0
# 	while not halt:
# 		ctr += 1
# 		halt = True
# 		for pair in dataPairs:
# 			halt = halt and solution.train(pair)
# 		# print(solution.weight)
# 		print("EPOCH = %d, %d errors left" %(ctr, solution.test(dataPairs)))

# 	return ctr




class PocketPLA(PLA):

	def __init__(self, config):

		PLA.__init__(self, config)

		self.pocketWeight = self.weight
		self.errors = np.inf


	def train(self, trainPair, testDataset):

		correct = super(PocketPLA, self).train(trainPair)

		errors = self.test(testDataset)

		# print(self.pocketWeight)

		if errors < self.errors:
			self.errors = errors
			self.pocketWeight = self.weight

		return correct

def hw1_pocket_random_cycles_sub(alpha, maxUpdate, exp_info):

	testDataset = np.loadtxt("./data/hw1_18_test.dat")
	dim, testDataPairs = PLA.makePairs(testDataset)

	trainingDataset = np.loadtxt("./data/hw1_18_train.dat")
	dim, trainingDataPairs = PLA.makePairs(trainingDataset)


	solution = PocketPLA({"dim": dim, "alpha": alpha})

	halt = False 
	updateCtr = 0

	seq = np.random.permutation(range(0, len(trainingDataset)))
	while not halt and updateCtr < maxUpdate:

		halt = True
		for i in seq:
			correct = solution.train(trainingDataPairs[i], testDataPairs)
			halt = halt and correct
			updateCtr += int(not correct)

	saveExp(str(solution.pocketWeight), updateCtr, alpha, exp_info)


def hw1_pocket_random_cycles(alpha, maxUpdate, exp_info, times):

	ts = int(time.time())
	for x in range(0, times):
		hw1_pocket_random_cycles_sub(alpha, maxUpdate, "%s-%d"%(exp_info, ts))






def hw1_15():
	dataset = np.loadtxt("./data/hw1_15_train.dat")

	dim, dataPairs = PLA.makePairs(dataset)


	solution = PLA({
			"dim": dim,
			"alpha": 1
		})

	halt = False
	updateCtr = 0
	while not halt:
		halt = True
		for pair in dataPairs:

			correct = solution.train(pair)
			halt = halt and correct
			updateCtr += int(not correct)

		# print(solution.weight)
		print("updateCtr = %d, %d errors left" %(updateCtr, solution.test(dataPairs)))

def hw1_random_cycles_sub(alpha, exp_info):

	dataset = np.loadtxt("./data/hw1_15_train.dat")

	dim, dataPairs = PLA.makePairs(dataset)


	solution = PLA({
			"dim": dim,
			"alpha": alpha
		})


	halt = False
	updateCtr = 0

	seq = np.random.permutation(range(0, len(dataset)))
	while not halt:
		halt = True

		for i in seq:
			correct = solution.train(dataPairs[i])
			halt = halt and correct
			updateCtr += int(not correct)

		# print("EPOCH = %d, %d errors left" %(ctr, solution.test(dataPairs)))
	saveExp(str(solution.weight), solution.errors, alpha, exp_info)

def hw1_histogram(exp_info, color = "blue"):

	global __conn, __cursor
	
	__cursor.execute('''SELECT halt_number FROM exp_record WHERE exp_info = :exp_info''', [exp_info])
	results = __cursor.fetchall()

	haltNumberArray = []
	for result in results:
		haltNumberArray.append(result["halt_number"])

	pl.hist(haltNumberArray, bins='auto', fc=color)  # plt.hist passes it's arguments to np.histogram
	pl.title("Histogram with halt number")
	pl.xlabel("number of updates")
	pl.ylabel("frequency")


def hw1_random_cycles(alpha, exp_info, times):

	ts = int(time.time())
	for x in range(0, times):
		hw1_random_cycles_sub(alpha, "%s-%d"%(exp_info, ts))




hw1_15()

# hw_17_sub()
# SQLiteDB = "./output/exp_records.db"
# SQLiteDB = os.path.join(os.path.dirname(__file__), SQLiteDB)
# iniGeneralSQLite(SQLiteDB)


# hw1_pocket_random_cycles(1, 50, "hw1_18", 2000)

# # # hw-16
# # hw1_random_cycles(1, "hw1_16", 2000)

# # # hw-17
# # hw1_random_cycles(0.25, "hw1_17", 2000)
# # # hw1_histogram("hw1_16-1481207743", (0, 0, 1, 0.3))
# # # hw1_histogram("hw1_17-1481207815", (1, 0, 0, 0.3))
# # pl.show()

# closeDB()


# hw1_17-1481206652
# hw1_16-1481207743
# hw1_17-1481207815