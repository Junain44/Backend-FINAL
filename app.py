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
        if request.method == 'POST':
            msg = None
            try:
                post_data = request.get_json()
                name = post_data['name']
                email = post_data['email']
                password = post_data['password']
                with sqlite3.connect('users.db') as conn:
                    cursor = conn.cursor()
                    conn.row_factory = dict_factory()
                    cursor.execute("INSERT INTO user(name, email, password) VALUES (?, ?, ?)",(name, email, password))
                    conn.commit()
                    msg = name + " was added to database "
            except Exception as e:
                msg = "Error in insertion " + str(e)
            finally:
                return {'msg': msg}


@app.route('/show/', methods=['GET'])
def show_user():
    try:
        with sqlite3.connect('users.db') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM user')
            rows= cursor.fetchall()
    except Exception as e:

        print("There was an error fetching results from the database: " + str(e))
    finally:
        connect.close()
        return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)




