
#Initializes the database, registers the bluePrint. !!!!! Dont add anything which is not needed across all packages !!!!!

from flask import Flask
from flaskext.mysql import MySQL

# local imports
from config import app_config

app = Flask(__name__)

mysql = MySQL()


# Creates the app based on the config provided, curretly the config_name is hard coded to development and uncomment the line which reads from the config file 
def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    
    # Gets the related config for the given key
    app.config.from_object(app_config[config_name])
    
    # Initialize the app
    mysql.init_app(app)

    # Import all the blue prints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .error import error as error_blueprint
    app.register_blueprint(error_blueprint)

    return app


# Run the app
if __name__ == "__main__":
    app.run()
