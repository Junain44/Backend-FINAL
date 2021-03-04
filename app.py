import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('users.db')
    print("database created succesfully")

    conn.execute('CREATE TABLE IF NOT EXISTS user(name TEXT, email TEXT, password TEXT)')
    print("Table created successfully")

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


@app.route('/add_user/', methods=['POST'])
def add_user():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user(name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            msg = name + " was added to database "
    except Exception as e:
        msg = "Error in insertion " + str(e)
    finally:
        conn.close()
    return jsonify(msg=msg)


@app.route('/show/', methods=['GET'])
def show_user():
    users = []
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


@app.route('/login/', methods=['GET'])
def login():
    msg = None
    try:
        email = request.form['mail']
        password = request.form['passw']

        with sqlite3.connect('users.db') as con:
            con.row_factory = dict_factory
            mycursor = con.cursor()
            mycursor.execute('SELECT * FROM user WHERE mail = ? and passw= ? and pin = ?', (email, password))
            data = mycursor.fetchone()
            msg = email + " has logged in."
    except Exception as e:
        con.rollback()
        msg = "There was a problem logging in try again later " + str(e)
    finally:
        con.close()
    return jsonify(data, msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
