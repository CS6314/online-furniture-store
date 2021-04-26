from flaskext.mysql import MySQL
import webApp

# To do create a helper method for executing the query, etc.
class database(object):
    @classmethod
    def connect(self):
        print("class method")
    
