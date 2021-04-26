# Package initialization file and !!!! don't add any routes here, add in the endpoints.py file !!!! 

from flask import Blueprint

admin = Blueprint('admin', __name__,template_folder='templates')

from . import endpoints
