import hw1exp
import numpy as np
import hw1io
import time

import os

global GLOBAL_TRAINING_DATAPAIRS
global GLOBAL_TEST_DATAPAIRS

global OUTPUT_DIR


def ini_problem(traingPath, testPath, outputDir, dbname):

	global GLOBAL_TRAINING_DATAPAIRS
	global GLOBAL_TEST_DATAPAIRS
	global OUTPUT_DIR


	GLOBAL_TRAINING_DATAPAIRS = hw1io.makePairs(traingPath)
	GLOBAL_TEST_DATAPAIRS = hw1io.makePairs(testPath)
	OUTPUT_DIR = outputDir

	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)

	SQLiteDB = os.path.join(OUTPUT_DIR, dbname)
	hw1io.iniSQLite(SQLiteDB)



# exp for problem 15, 16, 17
def problem_pla_exp(alpha, exp_category, random = False, rollNum = 0):

	global GLOBAL_TRAINING_DATAPAIRS
	global GLOBAL_TEST_DATAPAIRS

	perception_structure, numer_of_updates = hw1exp.pla_exp(GLOBAL_TRAINING_DATAPAIRS, alpha, random, rollNum)
	hw1io.saveExp(perception_structure, numer_of_updates, 0, alpha, exp_category)

# dig for problem 15, 16, 17
def problem_pla_digram(exp_category):

	global OUTPUT_DIR

	targetColumn = "numer_of_updates"
	diagramTitle = exp_category

	# % due to problem_15-xxxx
	sqlResult = hw1io.loadFromDb(exp_category + "%", targetColumn)
	hw1io.drawHistogram(sqlResult, targetColumn, diagramTitle, targetColumn, "frequency", OUTPUT_DIR)

# exp for problem 18, 19, 20
def problem_pocket_exp(alpha, maxUpdate, exp_category, usePocketWeight = True):

	global GLOBAL_TRAINING_DATAPAIRS
	global GLOBAL_TEST_DATAPAIRS

	perception_structure, errorRate = hw1exp.pocket_exp(GLOBAL_TRAINING_DATAPAIRS, GLOBAL_TEST_DATAPAIRS, 
		alpha=alpha, maxUpdate=maxUpdate, usePocketWeight=usePocketWeight)
	hw1io.saveExp(perception_structure, maxUpdate, errorRate, alpha, exp_category)

# dig for problem 18, 19, 20
def problem_pocket_digram(exp_category):

	global OUTPUT_DIR

	targetColumn = "err_rate"
	diagramTitle = exp_category

	sqlResult = hw1io.loadFromDb(exp_category + "%", targetColumn)
	hw1io.drawHistogram(sqlResult, targetColumn, diagramTitle, targetColumn, "frequency", OUTPUT_DIR)


def problem_15_exp():

	global GLOBAL_TRAINING_DATAPAIRS

	for i in range(0, len(GLOBAL_TRAINING_DATAPAIRS)):
		problem_pla_exp(1, "problem_15-roll_%d" %(i), False, i)


PROBLEM_ALGORITHM_MAP = {
	"15": {
		"exp": (problem_15_exp, []),
		"dig": (problem_pla_digram, ["problem_15"])
	},
	"16": {
		"exp": (problem_pla_exp, [1, "problem_16", True]),
		"dig": (problem_pla_digram, ["problem_16"])
	},
	"17": {
		"exp": (problem_pla_exp, [1, "problem_17", True]),
		"dig": (problem_pla_digram, ["problem_17"])
	},
	"18": {
		"exp": (problem_pocket_exp, [1, 50, "problem_18"]),
		"dig": (problem_pocket_digram, ["problem_18"])
	},
	"19": {
		"exp": (problem_pocket_exp, [1, 100, "problem_19"]),
		"dig": (problem_pocket_digram, ["problem_19"])
	},
	"20": {
		"exp": (problem_pocket_exp, [1, 100, "problem_20", False]),
		"dig": (problem_pocket_digram, ["problem_20"])
	}
}

PROBLEM_DATASET_MAP = {
	"15" : {
		"training_path": "data/hw1_15_train.dat",
		"test_path": "data/hw1_15_train.dat"
	},
	"16" : {
		"training_path": "data/hw1_15_train.dat",
		"test_path": "data/hw1_15_train.dat"
	},
	"17" : {
		"training_path": "data/hw1_15_train.dat",
		"test_path": "data/hw1_15_train.dat"
	},
	"18" : {
		"training_path": "data/hw1_18_train.dat",
		"test_path": "data/hw1_18_test.dat"
	},
	"19" : {
		"training_path": "data/hw1_18_train.dat",
		"test_path": "data/hw1_18_test.dat"
	},
	"20" : {
		"training_path": "data/hw1_18_train.dat",
		"test_path": "data/hw1_18_test.dat"
	}
}


def execute(fun, args):
	fun(*args)