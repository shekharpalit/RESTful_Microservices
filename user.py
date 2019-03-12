import os
from flask import Flask, request, jsonify, make_response, g, current_app, Response
from passlib.apps import custom_app_context as pwd_context
import sqlite3
import datetime
from flask_basicauth import BasicAuth
from functools import wraps


def hash_password(password):
    password_hash = pwd_context.encrypt(password)
    return password_hash

    def verify_password(password):
        return pwd_context.verify(password, password_hash)

def check_auth(username, password):
    cur = get_db().cursor().execute("SELECT user_name, hash_pwd from users WHERE user_name=?", (username,))
    row = cur.fetchall()
    if row[0][0] == username and row[0][1] == password:
        return True
    else:
        return False

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            if not uid or not pwd or check_auth(uid, pwd) == False:
                return authenticate()
            else:
                return f(*args, **kwargs)
        except:
            return "Need authentication for this opetation\n"
    return decorated

app = Flask(__name__)
DATABASE = 'test_user.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)  #create a database instance and use it for later execution
        print("database instance is created")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/createUser', methods=['POST'])
def createDB():
    conn = sqlite3.connect('test_user.db')
    c =conn.cursor()
    conn.execute('CREATE TABLE if not exists users (user_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT NOT NULL,  hash_pwd TEXT NOT NULL, name TEXT NOT NULL, email_id TEXT NOT NULL,  date_created DATE NOT NULL, is_active INTEGER NOT NULL)')

#remaining handle sql query fail and return the status codes
#create user other

@app.route('/user', methods=['POST'])
def InsertUser():
    if request.method == 'POST':
        executionState:bool = False
        cur = get_db().cursor()
        try:
            data =request.get_json(force= True)
            tmod = datetime.now()
            is_active = 1
            cur.execute("INSERT INTO users (user_name, hash_pwd, name, email_id, date_created, is_active ) VALUES (?, ?, ?, ?, ?, ?)",(data['user_name'], hash_password(data['hash_pwd']),data['name'],data['email_id'], tmod, is_active))
            if(cur.rowcount >=1):
                executionState = True
            get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data Instersted Sucessfully"), 200
            else:
                return jsonify(message="Failed to insert data"), 409




#update user

@app.route('/user', methods=['PATCH'])
@requires_auth
def UpdateUser():
    if request.method == 'PATCH':
        executionState:bool = False
        cur = get_db().cursor()
        try:
            data  = request.get_json(force=True)
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("UPDATE users SET hash_pwd=? WHERE user_name=? AND EXISTS(SELECT 1 FROM users WHERE user_name=? AND is_active=1)", (data['hash_pwd'], data['user_name'],data['user_name']))
            if(cur.rowcount >=1):
                executionState = True
                get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Updated SucessFully"), 200
            else:
                return jsonify(message="Failed to update the data"), 409


#delete user

@app.route('/user', methods=['DELETE'])
@requires_auth
def DeleteUser():
    if request.method =="DELETE":
        executionState:bool = False
        cur = get_db().cursor()
        try:
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("UPDATE users SET is_active =? WHERE user_name=? ", (0,uid))

            if cur.rowcount >= 1:
                executionState = True
            get_db().commit()

        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data SucessFully deleted"), 200
            else:
                return jsonify(message="Failed to delete data"), 409






if __name__== "__main__":
    app.run(debug=True, port=5000)
