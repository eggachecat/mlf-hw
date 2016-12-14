import numpy as np
import pylab as pl
import sqlite3
import os

global __conn, __cursor

def iniSQLite(dbPath):

	global __conn, __cursor

	newDB = False
	if not os.path.isfile(dbPath):
		newDB = True
	
	__conn = sqlite3.connect(dbPath)
	__conn.row_factory = sqlite3.Row
	__cursor = __conn.cursor()

	if newDB:
		createTable()


def createTable():

	global __cursor
	__cursor.execute('''CREATE TABLE exp_record
			            (exp_id INTEGER PRIMARY KEY NOT NULL, 
			            perception_structure TEXT, number_of_updates INTEGER, err_rate REAL, alpha INTEGER, 
			            exp_category TEXT)''')

def saveExp(perception_structure, number_of_updates, err_rate, alpha, exp_category):
	global __conn, __cursor
	
	__cursor.execute('''INSERT INTO exp_record(perception_structure, number_of_updates, err_rate, alpha, exp_category)
				 VALUES(?, ?, ?, ?, ?)''', (perception_structure, number_of_updates, err_rate, alpha, exp_category))

	__conn.commit()

def loadFromDb(exp_category, columns):

	global __conn, __cursor
	
	columnStr = str(columns).replace("'", "").replace("(", "").replace(")", "")
	base_query = "SELECT %s FROM exp_record WHERE exp_category LIKE :exp_category" % (columnStr)

	__cursor.execute(base_query, [exp_category])

	return __cursor.fetchall()


def closeDB():

	global __conn
	__conn.close()

def makePairs(dataPath):

	dataset = np.loadtxt(dataPath)

	pairs = []
	for row in dataset:
		splitIndex = len(row) - 1
		pairs.append({
			"input": row[0:splitIndex],
			"truth": row[splitIndex]
		})
	return pairs

def drawHistogram(sqlResults, key, title, xlabel, ylabel, outputDir):


	resultArray = []
	for result in sqlResults:
		resultArray.append(result[key])

	pl.hist(resultArray, bins='auto')
	pl.title(title)
	pl.xlabel(xlabel)
	pl.ylabel(ylabel)
	pl.savefig(("%s/%s.png")%(outputDir, title))
	print(("Saved result to %s/%s.png")%(outputDir, title))
