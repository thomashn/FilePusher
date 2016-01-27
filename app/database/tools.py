from .files import FileTable
from .users import UserTable

class Setup():
        
    def __init__(self,filePath):
        self.path = filePath
        self.ut = UserTable(self.path)
        self.ut.create()
        self.ft = FileTable(self.path)
        self.ft.create()

    def createRoot(self,username,password):
        self.ut.addUser(username,password)

