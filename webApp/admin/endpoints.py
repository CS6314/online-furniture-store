
# Contains all the endpoint related to the user authentication

from flask import render_template, redirect

from flask import render_template

from . import admin

# Renders the error.html page
@admin.route("/products")
def show():
    return render_template('shop.html', title='Shop Products')
