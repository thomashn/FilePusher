from sqlite3 import dbapi2 as sql

class Basic():
	""" A class inherited by other classes that is used
	to connect to the database by providing a file path """


	def __init__(self,filePath):
            self.db = sql.connect(filePath)
            self.cursor = self.db.cursor()

	def __del__(self):
	    self.db.close()
	

