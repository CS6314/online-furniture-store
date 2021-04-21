
from flask import Flask, render_template, request, json, redirect
from flaskext.mysql import MySQL
import views 
from flask import session


app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_PASSWORD'] = 'akash123'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'flask_todo_list'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

app.secret_key = 'secret key can be anything!'

# Send web pages


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/login')
def showSignUp():
    return render_template('login-register.html')


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@app.route('/userHome')
def userHome():

    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/showAddItem')
def showAddItem():
    todoId = request.args.get('id')
    if todoId is None:
        return render_template('addItem.html')
    else:
        # fetch the todo details from DB
        con = mysql.connect()
        cursor = con.cursor()

        cursor.execute(
            "SELECT id,title,description,isCompleted FROM tbl_todo WHERE id = %s", (todoId))

        data = cursor.fetchall()
        return render_template('addItem.html', id=data[0][0], inputTitle=data[0][1], inputDescription=data[0][2], isCompleted=data[0][3])

 #
 #  Validate login end point
 #


@app.route('/validateLogin', methods=['POST'])
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
                return redirect('/userHome')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()

#
#   Sign up end point
#


@app.route('/signUp', methods=['POST'])
def signUp():

    # read the form data
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the form data
    if _name and _email and _password:

        # Open mysql connection
        conn = mysql.connect()
        cursor = conn.cursor()

        # check the user whether he is registrated already or not
        cursor.execute("SELECT * FROM tbl_user WHERE email = %s", (_email))
        registeredUserDetails = cursor.fetchall()

        if len(registeredUserDetails) > 0:
            return json.dumps({'message': 'User already registered!'})

        # Pass the SQL statement
        cursor.execute(
            "INSERT INTO tbl_user(name, email, password) VALUES (%s, %s, %s)", (_name, _email, _password))

        # Confirm its inserted properly
        data = cursor.fetchall()

        if len(data) == 0:
            conn.commit()
            return json.dumps({'message': 'User created successfully !'})
        else:
            return json.dumps({'error': str(data[0])})

    else:
        return json.dumps({'html': '<span>Enter the required fields!</span>'})

#
#   # Add Item end point
#


@app.route('/addItem', methods=['POST'])
def addItem():

    try:
        if session.get('user'):
            todoId = request.args.get('id')
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
            isCompleted = 1 if len(
                request.form.getlist('isCompleted')) > 0 else 0
            print(isCompleted)
            conn = mysql.connect()
            cursor = conn.cursor()

            if todoId:
                # update the todo list with all the new fields
                cursor.execute("UPDATE tbl_todo SET title = %s,description = %s,isCompleted=%s WHERE (id = %s); ", (
                    _title, _description, (isCompleted), todoId))
            else:

                cursor.execute("INSERT INTO tbl_todo(title,description,userid,isCompleted) VALUES (%s, %s, %s,%s)", (
                    _title, _description, _user, (isCompleted)))

            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()

                return redirect('/userHome')

            else:
                return render_template('error.html', error="An error occured!")

        else:
            return render_template('error.html', error="Unauthorized Access")
    except Exception as e:
        return render_template('error.html', error=str(e))

#
# RetrieveData end point
#


@app.route('/retrieveData', methods=['GET'])
def retrieveData():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT * from tbl_todo WHERE userid = %s", (_user))

            data = cursor.fetchall()
            return json.dumps(data)
            # if len(data) == 0:
            #     return json.dumps(data)

            # else:
            #     return render_template('error.html', error = "An error occured!")

        else:
            return render_template('error.html', error="Unauthorized Access")
    except Exception as e:
        return render_template('error.html', error=str(e))

#
# Delete the to-do list item
#


@app.route('/deleteTodolistItem', methods=['GET'])
def deleteTheTodolist():

    try:
        if session.get('user'):
            # validate user, then delete the to do list
            todoId = request.args.get('id')

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM tbl_todo WHERE (id = %s); ", (todoId))

            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()

                return redirect('/userHome')

            else:
                return render_template('error.html', error="An error occured!")
    except Exception as e:
        return render_template('error.html', error=str(e))


# Run the app
if __name__ == "__main__":
    app.run()
