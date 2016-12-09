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