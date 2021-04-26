
# Contains all the endpoint related to the user authentication

from flask import render_template, redirect

from flask import render_template

from . import error

# Renders the error.html page
@error.route("/error")
def show():
    return render_template('error.html', title='error')
