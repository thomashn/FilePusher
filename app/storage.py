from os import remove
from os.path import isfile

class FileStorage():

        def __init__(self,root):
                self.root = str(root)
                self.path = None
                self.cFile = None

        def removeFile(self,path):
                fPath = self.__fullPath(path)
                if isfile(fPath):
                        print("Removing: "+str(fPath))
                        remove(fPath)

        def __fullPath(self,path):
                if self.root[-1] == "/":
                    return (self.root+str(path))
                else:
                    return (self.root+"/"+str(path))

        def openFile(self,path):
                self.path = str(path)
                fPath = self.__fullPath(path)
                self.cFile = open(fPath,'wb')
                return None

        def closeFile(self):
                if self.cFile:
                        self.cFile.close()
                        self.cFile = None
                        self.path = None

        def write2File(self,data):
                if self.cFile:
                        self.cFile.write(data)
                return None
