import cherrypy
class HelloWorld(object):
    def index(self):
        return 'HelloWorld'
    index.exposed = True
cherrypy.quickstart(HelloWorld())
