class Basic():
    def __init__(self,id,name):
        self.id = id
        self.name = name

class User(Basic):
    def __init__(self,id,name,password,salt):
        Basic.__init__(self,id,name)
        self.password = password
        self.salt = salt

class File(Basic):
    def __init__(self,id,name,URL,ownerId,maxDownloads,timesDownloaded):
        Basic.__init__(self,id,name)
        self.URL = URL
        self.maxDownloads = maxDownloads
        self.ownerId = ownerId
        self.fullPath = None
        self.timesDownloaded = timesDownloaded

