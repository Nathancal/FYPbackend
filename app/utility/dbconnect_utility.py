from werkzeug.wrappers import Response
import mongoengine
from config import Config



#This piece of middleware allows us to try and connect to the database by providing
#a wrapper function for the flask application, imported from API *
class DBConnect:
    def __init__(self, app):
        self.__app = app

    def __call__(self, environ, start_response):
        #Using mongoengine module the function connect is called and the database name and host are passed.
        #Logging is used to provide the developer with an indiciation of where the program passes/fails
        try:
            #DB connection information is stored in a Config file for an extra element of protection.
            mongoengine.connect(db=Config.MONGODB_SETTINGS["db"],
                                host=Config.MONGODB_SETTINGS["host"])


            return self.__app(environ, start_response)
        except ConnectionError as e:
            res = Response(u'Connection to mongo failed', mimetype='application/json', status=501)
            return res(environ, start_response)
