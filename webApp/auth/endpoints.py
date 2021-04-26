
# Contains all the endpoint related to the user authentication. Remove the unneccessary packages from the import

from flask import Flask, render_template, request, json, redirect, url_for, flash
from flask import session

from flask import render_template

from . import auth
from webApp import database
from .. import mysql


@auth.route("/login")
def showLoginPage():
    return render_template('login-register.html', title='Login')


# Validates the user credentials, To do:  sanitize the form inputs before appending to the query, to prevent SQL injection attacks
@auth.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM tbl_user WHERE email = %s", (_email))

        data = cursor.fetchall()

        if len(data) > 0:
            if str(data[0][3]) == _password:
                session['user'] = data[0][0]
                return redirect(url_for('home.dashboard'))
            else:
                # Send the error message to the user to display it as response
                flash('Wrong Email address or Password.')
                return redirect(url_for('auth.showLoginPage'))

                # Other ways of sending the data back to the user, DONT REMOVE THE COMMENTS
                # return redirect(url_for('error.show'))
                # return render_template('../error/templates/error.html', error='Wrong Email address or Password.')
        else:
            # Send the error message to the user to display it as response
            flash('Wrong Email address or Password.')
            return redirect(url_for('auth.showLoginPage'))

    except Exception as e:
        # Send the error message to the user to display it as response
        flash(str(e))
        return redirect(url_for('error.show'))
    finally:
        # Always close the Database connection
        cursor.close()
        con.close()
