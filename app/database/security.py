import hashlib 
from os import urandom


def generateSalt():
	""" The salt generator used for passwords """
	return urandom(512)

def addSalt(string,salt):
	""" Adds the binary salt with the binary string """
	string = str(string).encode("utf8")
	return string+salt

def doHash(string):
	""" Hash function used for password hashes """
	return hashlib.sha512(string).digest()
