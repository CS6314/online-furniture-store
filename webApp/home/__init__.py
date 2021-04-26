# Package initialization file and !!!! don't add any routes here !!!! 

from flask import Blueprint

home = Blueprint('home', __name__,template_folder='templates')

from . import endpoints
