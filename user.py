from flask import Flask, request
import sqlite3
import datetime
from flask_basicauth import BasicAuth
#from user import User

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'jon3'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True
@app.route('/')
@basic_auth.required
def auth():
    return "Authenticated"


@app.route('/createUser', methods=['POST'])
def createDB():
    conn = sqlite3.connect('test_user.db')
    c =conn.cursor()
    conn.execute('CREATE TABLE if not exists users (user_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT NOT NULL,  hash_pwd TEXT NOT NULL, name TEXT NOT NULL, email_id TEXT NOT NULL,  date_created DATE NOT NULL, is_active INTEGER NOT NULL)')

#remaining handle sql query fail and return the status codes
#create user other
@app.route('/user', methods=['POST'])

def insertUser():
    if request.method == 'POST':
        userData =request.get_json(force= True)
        date_created =datetime.date.today()
        is_active =1
        with sqlite3.connect('test_user.db') as conn:
            cur = conn.cursor()
            result = cur.execute("""INSERT INTO users (user_name, hash_pwd, name, email_id, date_created, is_active ) VALUES (:user_name,:hash_pwd,:name, :email_id, :date_created, :is_active )""",{"user_name":userData['user_name'], "hash_pwd":userData['hash_pwd'], "name":userData['name'], "email_id":userData['email_id'], "date_created":date_created,"is_active":is_active}).rowcount
            if (result >=1):
                return "User successfully added \n "
            else:
                return "Failed to add user"



#update user
@app.route('/user', methods=['PUT'])
def articles():
    if request.method == 'PUT':
        userData = request.get_json(force= True)
        with sqlite3.connect('test_user.db') as conn:
            cur =conn.cursor()
            result =cur.execute("""UPDATE users SET hash_pwd=:hash_pwd WHERE user_id=:user_id AND EXISTS(SELECT 1 FROM users WHERE user_id=:user_id AND is_active=1) """, {"hash_pwd":userData['hash_pwd'], "user_id":userData['user_id']}).rowcount
            if(result >=1):
                return "Password updated successfully"
            else:
                return "User does not exists \n "



#delete user
@app.route('/user', methods=['DELETE'])
def article():
    if request.method =="DELETE":
        userData = request.get_json(force= True)
        with sqlite3.connect('test_user.db') as conn:
            c =conn.cursor()
            result =c.execute("""UPDATE users SET is_active = :is_active WHERE user_id=:user_id """, {"is_active":0,"user_id":userData['user_id']}).rowcount
        if(result>=1):
            return "User Deleted Successfully"
        else:
            return "User Deletion Failed"



if __name__== "__main__":
    app.run(debug =True)
