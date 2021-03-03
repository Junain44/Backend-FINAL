import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

def init_sqlite_db():

    conn = sqlite3.connect('users.db')
    print("database created sucesfully")

    conn.execute('CREATE TABLE IF NOT EXISTS user(first_name TEXT, last_name TEXT, password TEXT)')
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


        # confirm_password=request.form['confirm']

                with sqlite3.connect('users.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO user(NAME, EMAIL, PASSWORD) VALUES (?, ?, ?)",
                                   (name, email, password))
                    conn.commit()
                    msg = name + " was added to database "

            except Exception as e:
                msg = "Error in insertion " + str(e)
            finally:
                return {'msg' : msg}


@app.route('/show/', methods=['GET'])
def show_students():
    admin = ()
    try:
        with sqlite3.connect('users.db') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM user')
            admin = cursor.fetchall()
    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        connect.close()
        return jsonify(show_students)

if __name__ == '__main__':
    app.run(debug=True)




