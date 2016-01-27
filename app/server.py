from os.path import isfile 
from configparser import ConfigParser

import cherrypy

from .database.tools import Setup
from .web.html import makeHTMLFileTable
from .web.security import reqAuth
from .operations import ServerOperations

cherrypy.tools.reqAuth = cherrypy.Tool('before_handler',reqAuth)


class FilePusher(object):
    def __init__(self,serverOperations):
        self.srv = serverOperations

    @cherrypy.expose
    @cherrypy.tools.reqAuth()
    def index(self):
        self.srv.removeExpiredFiles()
        files = self.srv.getListOfUserFiles(cherrypy.session['userId']) 
        page = """  
<html>
<head></head>
<body>
<p>Welcome, you are logged in as '"""+cherrypy.session['name']+"""'</p>
<form method="post" action="upload" enctype="multipart/form-data">
<input type="text" name="downloads" value=1 />
<input type="file" name="filedata" />
<button type="submit">Submit</button>
</form>
"""+makeHTMLFileTable(files)+"""	
</body>
</html>
"""
        return page

    @cherrypy.expose
    def download(self,fileURL):
        self.srv.removeExpiredFiles()
        _file = self.srv.prepareFileForDownload(fileURL)
        if _file:
            return cherrypy.lib.static.serve_file(_file.fullPath,
                "application/x-download", "attachment",_file.name)
        else:
            raise cherrypy.HTTPError(401) 

    @cherrypy.expose
    @cherrypy.tools.reqAuth()
    def upload(self,filedata,downloads):
        while True:
            url = self.srv.generateURL()
            if self.srv.noDuplicates(url): 
                userId = cherrypy.session['userId']
                self.srv.saveFileToServer(filedata,url,userId,downloads)
                break
        raise cherrypy.HTTPRedirect("index")	

    @cherrypy.expose
    def delete(self,fileURL):
        self.srv.removeFileFromServer(fileURL)
        raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def authenticate(self,user,passwd):
        validUser = self.srv.confirmUserLogin(user,passwd)
        if validUser:
            cherrypy.engine.log("User '"+validUser.name+"' authenticated!")
            cherrypy.session['userId'] = validUser.id
            cherrypy.session['name'] = validUser.name
            raise cherrypy.HTTPRedirect("index")
        raise cherrypy.HTTPRedirect("login")

    @cherrypy.expose
    def login(self):
        page = """
<html>
<head></head>
<body>
<form method="post" action="authenticate" enctype="multipart/form-data">
<input type="text" name="user" />
<input type="password" name="passwd" />
<button type="submit">Login!</button>
</form>
</body>
</html>
"""
        return page

