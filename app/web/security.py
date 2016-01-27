import cherrypy


def reqAuth():
	if 'userId' in cherrypy.session:
		return False
	else:
		raise cherrypy.HTTPRedirect("/login")
