import hw1exp
import numpy as np
import hw1io
import time

import os
# dataPairs = hw1io.makePairs("./data/hw1_15_train.dat")
# hw1exp.pla_exp(dataPairs, alpha = 1, exp_info = "hw1_15")



outputDir = "output"
outputDir = os.path.join(os.path.dirname(__file__), outputDir)

if not os.path.exists(outputDir):
	os.makedirs(outputDir)

SQLiteDB = os.path.join(outputDir, "exp_records.db")
hw1io.iniSQLite(SQLiteDB)

dataset = hw1io.makePairs("./data/hw1_15_train.dat")

trainingDataPairs = hw1io.makePairs("./data/hw1_18_train.dat")
testDataPairs = hw1io.makePairs("./data/hw1_18_test.dat")


def problem_pla(alpha, exp_category, random = False, rollNum = 0):

	perception_structure, numer_of_updates = hw1exp.pla_exp(dataset, alpha, random, rollNum)

	hw1io.saveExp(perception_structure, numer_of_updates, 0, alpha, exp_category)

def problem_pocket(alpha, maxUpdate, exp_category, usePocketWeight = True):

	perception_structure, errorRate = hw1exp.pocket_exp(trainingDataPairs, testDataPairs, 
		alpha=alpha, maxUpdate=maxUpdate, usePocketWeight=usePocketWeight)

	hw1io.saveExp(perception_structure, maxUpdate, errorRate, alpha, exp_category)



def problem_15():
	for i in range(0, len(dataset)):
		problem_pla(1, "problem_15-roll_%d" %(i), False, i)

def problem_16():
	problem_pla(1, "problem_16", True)

def problem_17():
	problem_pla(0.25, "problem_17", True)



def problem_18():
	problem_pocket(1, 50, "problem_18")

def problem_19():
	problem_pocket(1, 100, "problem_19")

def problem_20():
	problem_pocket(1, 100, "problem_20", usePocketWeight = False)


# problem_15()
while True:
	problem_16()
	problem_17()


# targetColumn = "err_rate"
# sqlResult = hw1io.loadFromDb("problem_20", targetColumn)
# hw1io.drawHistogram(sqlResult, targetColumn, xlabel=targetColumn, ylabel="frequency")
