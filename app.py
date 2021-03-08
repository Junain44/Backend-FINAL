import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


def init_sqlite_db():
    # Connects the to the database
    conn = sqlite3.connect('users.db')
    print("database created succesfully")

    # Creates the table for the users
    conn.execute('CREATE TABLE IF NOT EXISTS user(name TEXT, email TEXT, password TEXT)')
    print("Table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS products(name TEXT, description TEXT, price TEXT, image TEXT)')
    print("Product table created successfully")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")

    print(cursor.fetchall())
    # conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
@app.route('/reg/', methods=['GET'])
def register():
    return render_template('register.html')


# Function that adds all the users
@app.route('/add_user/', methods=['POST'])
def add_user():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user(name, email, password) VALUES (?, ?, ?)', (name, email, password))
            conn.commit()
            msg = name + "was added to database"
    except Exception as e:
        msg = "Error in insertion" + str(e)
    finally:
         conn.close()
    return jsonify(msg=msg)


# The function that shows all the users that registered
@app.route('/show/', methods=['GET'])
def show_user():
    msg = None
    try:
        with sqlite3.connect('users.db') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM user")
            users = cursor.fetchall()
    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        connect.close()
    return jsonify(users)


# @app.route('/add_products/', methods=['POST'])
# def add_products():
#     with sqlite3.connect('users.db') as conn:
#         cursor = conn.cursor()
#         conn.row_factory = dict_factory
#
#         # Adding the T-shirts
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS RED T-SHIRT', 'R350.00', 'https://i.postimg.cc/v8WhgTbL/shirt1.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS WHITE T-SHIRT', 'R150.00', 'https://i.postimg.cc/MTm1KsQk/shirt2.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS WHITE T-SHIRT', 'R250.00', 'https://i.postimg.cc/gJtkD89X/shirt3.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS WHITE T-SHIRT', 'R450.00', 'https://i.postimg.cc/XvR07L0g/shirt4.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS BLACK T-SHIRT', 'R650.00', 'https://i.postimg.cc/G2F631Kc/shirt5.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS BLACK T-SHIRT', 'R250.00', 'https://i.postimg.cc/bNBVhJPx/shirt6.jpg'))
#
#         # Adding the jeans
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS BLACK JEANS', 'R350.00', 'https://i.postimg.cc/jqzJTkrZ/jean1.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS BLACK JEANS', 'R500.00', 'https://i.postimg.cc/mrzt5mw3/jean2.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS GREY JEANS', 'R250.00', 'https://i.postimg.cc/02Vj5TXd/jean3.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS GREY JEANS', 'R150.00', 'https://i.postimg.cc/VNDDKLK0/jean4.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS BLUE JEANS', 'R150.00', 'https://i.postimg.cc/XqQ5bpy9/jean5.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL MENS BLUE JEANS', 'R150.00', 'https://i.postimg.cc/52ZCbcjK/jean6.jpg'))
#
#
#         # Adding the shoes
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL BLACK SNEAKER', 'R1,999.95', 'https://i.postimg.cc/bYW86q55/shoe1.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL BLACK SNEAKER', 'R2,999.95', 'https://i.postimg.cc/xd6VLQHt/shoe2.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL BLACK SUPERGA', 'R999.95', 'https://i.postimg.cc/Kz4SNWDF/shoe3.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL BLACK UZZI', 'R899.95', 'https://i.postimg.cc/CxYKNFBg/shoe4.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL WHITE ADIDAS', 'R659.95', 'https://i.postimg.cc/ryrF2d5T/shoe5.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL BLACK SUPERGA', 'R799.95', 'https://i.postimg.cc/jdRV3CXZ/shoe6.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL BLACK SUPERGA', 'R399.95', 'https://i.postimg.cc/NFj6LWmh/shoe7.jpg'))
#         cursor.execute("INSERT INTO products(name, description, price, image) VALUES (?, ?, ?, ?)", ('ADIDAS', 'ORIGINAL BLACK SUPERGA', 'R499.95', 'https://i.postimg.cc/dtDRFcJr/shoe8.jpg'))
#         conn.commit()
#
# add_products()


@app.route('/show_products/', methods=['GET'])
def show_products():
    msg = None
    try:
        with sqlite3.connect('users.db') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM products")
            users = cursor.fetchall()
    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        connect.close()
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)
