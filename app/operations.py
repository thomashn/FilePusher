import random
import string

from .database.files import FileTable
from .database.users import UserTable
from .storage import FileStorage


class ServerOperations():
    def __init__(self,database,filesFolder):
        self.database = database
        self.folder = filesFolder

    def getListOfUserFiles(self,uid):
        ft = FileTable(self.database)
        files = ft.getFilesWithOwnerId(uid)
        return files

    def confirmUserLogin(self,username,password):
        return UserTable(self.database).authenticateUser(username,password)

    def removeExpiredFiles(self):
        ft = FileTable(self.database)
        for expiredFile in ft.findExpiredFiles():
            self.removeFileFromServer(expiredFile.URL)

    def removeFileFromServer(self,fileURL):
        fs = FileStorage(self.folder)
        ft = FileTable(self.database)
        ft.removeFileWithURL(fileURL)
        fs.removeFile(fileURL)

    def prepareFileForDownload(self,fileURL):
        ft = FileTable(self.database)
        match = ft.getFileWithURL(fileURL)
        if match:
            match.fullPath = self.folder+"/"+fileURL
            ft.registerDownload(match.id)
            return match
        else:
            return None

    def generateURL(self):
        possible = list(string.ascii_lowercase)
        possible.extend(list(string.digits))
        possible.extend(list(string.ascii_uppercase))
        url = ""
        for i in range(0,23):
            letter = random.randint(0,len(possible)-1)
            url += possible[letter]
        return url 

    def noDuplicates(self,fileURL):
        if FileTable(self.database).getFileWithURL(fileURL):
            return False
        else:
            return True

    def saveFileToServer(self,filedata,url,userId,downloads):
        fs = FileStorage(self.folder)
        fs.openFile(url)
        while True:
            block = filedata.file.read(8192)
            fs.write2File(block)
            if not block:
                break
        fs.closeFile()
        
        try:
            downloads = int(downloads)
        except:
            downloads = 0

        fileName = filedata.filename
        FileTable(self.database).addFile(fileName,url,userId,downloads)

