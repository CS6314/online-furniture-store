
from flask import Flask, render_template, request, json, redirect
from flaskext.mysql import MySQL
import views 
from flask import session
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static\images\product'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)


mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'furniturestore'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
mysql.init_app(app)

app.secret_key = 'secret key can be anything!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Send web pages


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/login')
def showSignUp():
    return render_template('login-register.html')

@app.route('/cart')
def showCart():
    return render_template('cart.html')

@app.route('/allProducts')
def allProducts():
    return render_template('all-products.html')

@app.route('/addProduct')
def addProduct():
    return render_template('add-product.html')

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@app.route('/home')
def userHome():

    if session.get('user'):
        return render_template('index.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/adminHome')
def adminHome():
    return render_template('adminHome.html')

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
@app.route('/getCart',methods=['GET'])
def getCart():
    try:
        _user = session.get('user')
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT p.product_id,p.title,p.description,p.image_name,c.quantity,p.quantity,p.price FROM product p , cart c WHERE p.product_id = c.product_id")
        data = cursor.fetchall()
        if len(data) > 0:
            return json.dumps(data)
        else:
            return json.dumps({'html':'<span> Cart Empty for User </span>'})
    
    except Exception as e:
            return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/getProducts',methods=['GET'])
def getProducts():
    try:
        _user = session.get('user')
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM product p")
        data = cursor.fetchall()
        if len(data) > 0:
            return json.dumps(data)
        else:
            return json.dumps({'html':'<span> No Products in the database </span>'})
    
    except Exception as e:
            return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/editProduct',methods=['POST'])
def editProduct():
    try :
        _productId = request.form['productId']
        _productName = request.form['productName']
        _productDescription = request.form['productDescription']
        _price = request.form['price']
        _quantity = request.form['quantity']
        _category = request.form['category']
        _isDeleted = request.form['isDeleted']
        
        print(_productId,_productName,_productDescription,_price,_quantity,_category,_isDeleted)
        
        conn = mysql.connect()
        cursor = conn.cursor()
        if 'image' in request.files:
            _imageFileName = request.files['image']
            filename = secure_filename(_imageFileName.filename)
            _imageFileName.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # ***TODO SAVE FILE TO FOLDER ON SERVER***
            # _imageFile.save(dirname, _imageFileName)
            
            
            # validate the received values
        if _productId :
            print("before sql")
            if _imageFileName:
                cursor.execute("UPDATE  product SET title = %s, description =%s, image_name = %s, price = %s, quantity = %s,category = %s,is_deleted = %s WHERE product_id =%s", (_productName, _productDescription, filename,_price,_quantity,_category,_isDeleted,_productId))
            else :
                cursor.execute("UPDATE  product SET title = %s, description =%s, price = %s, quantity = %s,category = %s,is_deleted = %s WHERE product_id =%s", (_productName, _productDescription,_price,_quantity,_category,_isDeleted,_productId))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
                return redirect('/allProducts')
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span> Product ID not recieved</span>'})
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/saveNewProduct',methods=['POST'])
def saveNewProduct():
    try :
        _productName = request.form['productName']
        _productDescription = request.form['productDescription']
        _price = request.form['price']
        _quantity = request.form['quantity']
        _category = request.form['category']
        _isDeleted = request.form['isDeleted']
        
        print(_productName,_productDescription,_price,_quantity,_category,_isDeleted)
        
        conn = mysql.connect()
        cursor = conn.cursor()
        if 'image' in request.files:

            _imageFileName = request.files['image']
            filename = secure_filename(_imageFileName.filename)
            _imageFileName.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            
            # validate the received values
        
        print("before sql")
        cursor.execute("INSERT INTO  product (title, description, image_name, price, quantity, category, is_deleted) VALUES ( %s, %s, %s, %s, %s, %s, %s)", (_productName, _productDescription, filename,_price,_quantity,_category,_isDeleted,))
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            return redirect('/allProducts')
        else:
            return json.dumps({'error':str(data[0])})
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/deleteProductFromCart',methods=['POST'])
def deleteProductFromCart():
    try :
        con = mysql.connect()
        cursor = con.cursor()
        # read the posted values from the UI
        requestBody = request.get_json()
        _productId = requestBody['productId']        
        # validate the received values
        if _productId :
            cursor.execute("DELETE FROM cart WHERE product_id = %s", (_productId))
            data = cursor.fetchall()
            if len(data) == 0:
                con.commit()
                return json.dumps({'delete':'successful'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span> Product ID to from Cart not received. </span>'})
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/increaseProductQuantityInCart',methods=['POST'])
def increaseProductQuantityInCart():
    try :
        con = mysql.connect()
        cursor = con.cursor()
        # read the posted values from the UI
        requestBody = request.get_json()
        _productId = requestBody['productId']
        _quantity = requestBody['quantity']        
        # validate the received values
        if _productId and _quantity:
            cursor.execute("UPDATE CART SET QUANTITY = %s WHERE product_id = %s", (_quantity,_productId))
            data = cursor.fetchall()
            if len(data) == 0:
                con.commit()
                return json.dumps({'update':'successful'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span> Product ID or Quanity to change from cart not received. </span>'})
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM user WHERE email = %s", (_email))

        data = cursor.fetchall()

        if len(data) > 0:
            if str(data[0][5]) == _password and data[0][6] == 0:
                session['user'] = data[0][0]
                return redirect('/home')
            if str(data[0][5]) == _password:
                session['user'] = data[0][0]
                return redirect('/adminHome')
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
    _firstname = request.form['firstName']
    _lastname =  request.form['lastName']
    _email =  request.form['inputEmail']
    _contactNumber =  request.form['contactNumber']
    _password =  request.form['inputPassword']
    # validate the form data
    if _firstname and _lastname and _email and _contactNumber and _password:

        # Open mysql connection
        conn = mysql.connect()
        cursor = conn.cursor()

        # check the user whether he is registrated already or not
        cursor.execute("SELECT * FROM user WHERE email = %s", (_email))
        registeredUserDetails = cursor.fetchall()

        if len(registeredUserDetails) > 0:
            return json.dumps({'message': 'User already registered!'})

        # Pass the SQL statement
        cursor.execute(
            "INSERT INTO user(email, fname, lname, contact, password) VALUES (%s, %s, %s, %s,%s)", (_email, _firstname, _lastname, _contactNumber, _password))

        # Confirm its inserted properly
        data = cursor.fetchall()

        if len(data) == 0:
            conn.commit()
            return redirect('/login')
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
