from .entries import File
from .connection import Basic


class FileTable(Basic):
    """ Manages file metadata.

    Responsible for managing the metadata related to
    files uploaded to the web server. This means adding and
    removing file metadata as well as detecting files that 
    are expired."""
    def __init__(self,database):
        Basic.__init__(self,database)

    def create(self):
        """Create table for file metadata"""
        cmd = ("CREATE TABLE files (id INTEGER PRIMARY KEY, filename, "
                "url, owner_id,max_downloads,times_downloaded INTEGER)")
        self.cursor.execute(cmd)
        self.db.commit()
    
    def addFile(self,name,URL,ownerId,downloadsMax):
        """Add a file entry into the filelist"""
        cmd = ("INSERT INTO files (filename, url, owner_id,"
            "max_downloads,times_downloaded) VALUES (?,?,?,?,0)")
        self.cursor.execute(cmd, (name,str(URL),str(ownerId),downloadsMax))
        self.db.commit()
        return None
    
    def getFilesWithOwnerId(self,ownerId):
        """Returns a list of File objects with matching owner id."""
        cmd = ("SELECT * FROM files WHERE owner_id=?")
        self.cursor.execute(cmd,(str(ownerId),))
        files = list()
        for f in self.cursor.fetchall():
                files.append(self.__parseFile(f))
        return files

    def getFileWithURL(self,URL):
        """Returns a single File object that has a matching URL."""
        cmd = ("SELECT * FROM files WHERE url=?")
        self.cursor.execute(cmd,(URL,))
        result = self.cursor.fetchone()
        if result:
            return self.__parseFile(result)    
        else:
            return None

    def findExpiredFiles(self):
        """Returns File objects that meet the *expired* conditions."""
        cmd = ("SELECT * FROM files WHERE times_downloaded >= max_downloads")
        self.cursor.execute(cmd)
        fTuple = list()
        for expired in self.cursor.fetchall():
                fTuple.append(self.__parseFile(expired))
        return fTuple

    def removeFileWithURL(self,URLs):
        """Removes a file matching the given URL"""
        URLs = self.__convert2List(URLs)
        cmd = ("DELETE FROM files WHERE url=?") 
        for URL in URLs:
            self.cursor.execute(cmd,(URL,))
        self.db.commit()

    def registerDownload(self,fileId):
        """Decrements the download counter for a file"""
        cmd = ("UPDATE files SET "
            "times_downloaded=times_downloaded + 1"
            " WHERE id=?")
        self.cursor.execute(cmd,(fileId,))
        self.db.commit()

    def __convert2List(self,variable):
        if variable is not list:
            return [variable]
        return variable

    def __parseFile(self,x):
        fId, name, URL, ownerId, maxdl, tdl= x
        return File(fId,name,URL,ownerId,maxdl,tdl)

    def __removeExpiredFiles(self):
        expiredFiles = self.findExpiredFiles()
        for f in expiredFiles:
            self.deleteEntryWithPath(f)

