
# Contains all the endpoint related to the user authentication, Remove the unneccessary packages from the import

from flask import Flask, render_template, request, json, redirect
from flask import session

from flask import render_template

from . import home
from webApp import database
from .. import mysql


@home.route("/userHome")
def dashboard():
    return render_template('blog.html', title='Home')
