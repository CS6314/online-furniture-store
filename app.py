
from flask import Flask, render_template, request, json, redirect
from flaskext.mysql import MySQL
import views
from flask import session
import os
from werkzeug.utils import secure_filename
import cryptocode

UPLOAD_FOLDER = 'static\images\product'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)


mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'furniture_store'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

app.secret_key = 'secret key can be anything!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Send web pages


@app.route("/")
def main():
    return render_template('login-register.html')


@app.route('/login')
def showSignUp():
    return render_template('login-register.html')

@app.route('/contact')
def showContact():
    return render_template('contact.html')

@app.route('/cart')
def showCart():
    if session.get('user'):
        return render_template('cart.html')
    else:
        return render_template('login-register.html')

@app.route('/orders')
def orders():
    if session.get('user'):
        return render_template('orders.html')
    else:
        return render_template('login-register.html')


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
def home():

    if session.get('user'):
        return render_template('index.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/adminHome')
def adminHome():
    if session.get('user'):
        if session.get('isAdmin')== 1:
            return render_template('adminHome.html')
        else:
            return render_template('user-home.html')
    else:
        return render_template('login-register.html')


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('user-home.html')
    else:
        return render_template('login-register.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


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


@app.route('/getCart', methods=['GET'])
def getCart():
    try:
        _user = session.get('user')
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT p.product_id,p.title,p.description,p.image_name,c.quantity,p.quantity,p.price FROM product p , cart c WHERE p.product_id = c.product_id and c.userid = %s",_user)
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

@app.route('/getOrders',methods=['GET'])
def getOrders():
    try:
        _user = session.get('user')
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT o.orderid,p.title,p.image_name,o.ordered_date,o.delivery_date,o.price,o.quantity,a.name,a.street,a.city,a.state,a.zipcode,a.phone FROM product p , orders o , address a WHERE p.product_id = o.productid and a.orderid = o.orderid and o.userid = %s",_user)
        data = cursor.fetchall()
        if len(data) > 0:
            return json.dumps(data)
        else:
            return json.dumps({'html': '<span> Cart Empty for User </span>'})

    except Exception as e:
            return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/getProducts', methods=['GET'])
def getProducts():
    try:
        _user = session.get('user')
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM product p order by product_id")
        data = cursor.fetchall()
        if len(data) > 0:
            return json.dumps(data)
        else:
            return json.dumps({'html': '<span> No Products in the database </span>'})

    except Exception as e:
            return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/getProductsForUser', methods=['GET'])
def getProductsForUser():
    try:
        _user = session.get('user')
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM product p where is_deleted=0 order by product_id")
        data = cursor.fetchall()
        if len(data) > 0:
            return json.dumps(data)
        else:
            return json.dumps({'html': '<span> No Products in the database </span>'})

    except Exception as e:
            return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/editProduct', methods=['POST'])
def editProduct():
    try:
        _productId = request.form['productId']
        _productName = request.form['productName']
        _productDescription = request.form['productDescription']
        _price = request.form['price']
        _quantity = request.form['quantity']
        _category = request.form['category']
        _isDeleted = request.form['isDeleted']

        print(_productId, _productName, _productDescription,
              _price, _quantity, _category, _isDeleted)

        conn = mysql.connect()
        cursor = conn.cursor()
        _imageFileName = request.files['image']
        if 'image' in request.files and request.files['image'].filename != '':
            _imageFileName = request.files['image']
            filename = secure_filename(_imageFileName.filename)
            _imageFileName.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            # ***TODO SAVE FILE TO FOLDER ON SERVER***
            # _imageFile.save(dirname, _imageFileName)

            # validate the received values
        if _productId:
            print("before sql")
            if _imageFileName:
                cursor.execute("UPDATE  product SET title = %s, description =%s, image_name = %s, price = %s, quantity = %s,category = %s,is_deleted = %s WHERE product_id =%s", (
                    _productName, _productDescription, filename, _price, _quantity, _category, _isDeleted, _productId))
            else:
                cursor.execute("UPDATE  product SET title = %s, description =%s, price = %s, quantity = %s,category = %s,is_deleted = %s WHERE product_id =%s", (
                    _productName, _productDescription, _price, _quantity, _category, _isDeleted, _productId))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
                return redirect('/allProducts')
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span> Product ID not recieved</span>'})
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/saveNewProduct', methods=['POST'])
def saveNewProduct():
    try:
        _productName = request.form['productName']
        _productDescription = request.form['productDescription']
        _price = request.form['price']
        _quantity = request.form['quantity']
        _category = request.form['category']
        _isDeleted = request.form['isDeleted'] if "isDeleted" in request.form else 0

        print(_productName, _productDescription,
              _price, _quantity, _category, _isDeleted)

        conn = mysql.connect()
        cursor = conn.cursor()
        if 'image' in request.files:

            _imageFileName = request.files['image']
            filename = secure_filename(_imageFileName.filename)
            _imageFileName.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))

        cursor.execute("INSERT INTO  product (title, description, image_name, price, quantity, category, is_deleted) VALUES ( %s, %s, %s, %s, %s, %s, %s)",
                       (_productName, _productDescription, filename, _price, _quantity, _category, _isDeleted,))
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            return redirect('/allProducts')
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/addToCart', methods=['POST'])
def addToCart():
    try:
        _user = session.get('user')
        _productId = request.form['productId']
        _quantity = 1

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM cart WHERE product_id = %s and userid = %s ",(_productId, _user))
        data = cursor.fetchall()
        if data :
            dbQuantity = data[0][0]
            if dbQuantity > 0 :
                dbQuantity = dbQuantity + 1
                cursor.execute("UPDATE cart SET quantity = %s where product_id =%s and userid =%s",(dbQuantity,_productId, _user)) 
        else:
            cursor.execute("INSERT INTO  cart (product_id, quantity, userid) VALUES ( %s, %s, %s)",(_productId,_quantity, _user))
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            return redirect('/cart')
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/deleteProductFromCart', methods=['POST'])
def deleteProductFromCart():
    try:
        con = mysql.connect()
        cursor = con.cursor()
        # read the posted values from the UI
        requestBody = request.get_json()
        _productId = requestBody['productId']
        # validate the received values
        if _productId:
            cursor.execute(
                "DELETE FROM cart WHERE product_id = %s", (_productId))
            data = cursor.fetchall()
            if len(data) == 0:
                con.commit()
                return json.dumps({'delete': 'successful'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span> Product ID to from Cart not received. </span>'})
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/increaseProductQuantityInCart', methods=['POST'])
def increaseProductQuantityInCart():
    try:
        con = mysql.connect()
        cursor = con.cursor()
        # read the posted values from the UI
        requestBody = request.get_json()
        _productId = requestBody['productId']
        _quantity = requestBody['quantity']
        # validate the received values
        if _productId and _quantity:
            cursor.execute(
                "UPDATE CART SET QUANTITY = %s WHERE product_id = %s", (_quantity, _productId))
            data = cursor.fetchall()
            if len(data) == 0:
                con.commit()
                return json.dumps({'update': 'successful'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span> Product ID or Quanity to change from cart not received. </span>'})
    except Exception as e:
        return render_template('error.html', error=str(e))
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
            _decryptedPassword = cryptocode.decrypt(str(data[0][5]),"ecryptionDecryptionKey")
            if _decryptedPassword == _password and data[0][6] == 0:
                session['user'] = data[0][0]
                return redirect('/userHome')
            if _decryptedPassword == _password:
                session['user'] = data[0][0]
                session['isAdmin'] = 1
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
    _lastname = request.form['lastName']
    _email = request.form['email']
    _contactNumber = request.form['contactNumber']
    _password = request.form['password']
    _encryptedPassword = cryptocode.encrypt(_password,"ecryptionDecryptionKey")
    # validate the form data
    if _firstname and _lastname and _email and _contactNumber and _password:

        # Open mysql connection
        conn = mysql.connect()
        cursor = conn.cursor()

        # check the user whether he is registrated already or not
        cursor.execute("SELECT * FROM user WHERE email = %s", (_email))
        registeredUserDetails = cursor.fetchall()

        if len(registeredUserDetails) > 0:
            return json.dumps({'error': 'User already registered!'})

        # Pass the SQL statement
        cursor.execute(
            "INSERT INTO user(email, fname, lname, contact, password) VALUES (%s, %s, %s, %s,%s)", (_email, _firstname, _lastname, _contactNumber, _encryptedPassword))

        # Confirm its inserted properly
        data = cursor.fetchall()

        if len(data) == 0:
            conn.commit()
            return json.dumps({'message': 'User registered!'})
        else:
            return json.dumps({'error': str(data[0])})

    else:
        return json.dumps({'html': '<span>Enter the required fields!</span>'})


#
# Retrieve category end point
#

@app.route('/categories', methods=['GET'])
def categories():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT distinct category from product")

            data = cursor.fetchall()
            return json.dumps(data)
        else:
            return render_template('error.html', error="Unauthorized Access")
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/searchProducts', methods=['POST'])
def searchProducts():
    try:

        filterValues = []

        baseQuery = 'SELECT * FROM product WHERE is_deleted = 0 '

        if request.form['searchText'] != '*' and request.form['searchText'] != '':
            baseQuery += 'AND (title like %s OR description like %s) '
            filterValues.extend(
                (('%'+request.form['searchText'].lower()+'%'), ('%'+request.form['searchText'].lower()+'%')))

        # If the user wants all item
        if request.form['category'] != '*' and request.form['category'] != '':
            baseQuery += 'AND category = %s '
            filterValues.append(request.form['category'])

        if request.form['price'] != '*' and request.form['price'] != '':
             if request.form['price'] == '100':
                baseQuery += 'AND (price > %s)'
                filterValues.append(100)
             else:
                baseQuery += 'AND  (price between %s AND %s)'
                filterValues.extend((request.form['price'].split('-')))

        if request.form['quantity'] != '*' and request.form['quantity'] != '':
            if request.form['quantity'] == '10':
                baseQuery += 'AND (quantity > %s)'
                filterValues.append(10)
            else:
                baseQuery += 'AND  (quantity between %s AND %s)'
                filterValues.extend((request.form['quantity'].split('-')))
        

        if type(request.args.get('pageNumber')) != type(None) :
            print (type(request.args.get('pageNumber')),'Value:',request.args.get('pageNumber'))
        # request.args.get('pageNumber') is not None: 
            pageNumber = int(request.args.get('pageNumber'))
            startingElement = 0 if 10*(pageNumber-1)-(pageNumber - 1) < 0 else 10*(pageNumber-1)-(pageNumber - 1)
            lastElement =  9 if startingElement == 0 else 10*(pageNumber)-pageNumber
            baseQuery += ' order by product_id LIMIT %s,%s '
            filterValues.extend((startingElement, lastElement))
        
        con = mysql.connect()
        cursor = con.cursor()
        print(baseQuery,filterValues)

        cursor.execute(baseQuery,
                       (filterValues))

        data = cursor.fetchall()
        print(cursor._last_executed)

        if len(data) > 0:
            return json.dumps(data)
        else:
            return json.dumps({'html': '<span> No Products in the database </span>'})

    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


# Run the app
if __name__ == "__main__":
    app.run()
