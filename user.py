from flask import Flask, request, jsonify, g, Response
from passlib.apps import custom_app_context as pwd_context
import sqlite3
import datetime
from authentication import check_auth,authenticate,requires_auth
from DatabaseInstance import get_db

app = Flask(__name__)


#remaining handle sql query fail and return the status codes
#create user other

@app.route('/user', methods=['POST'])
def InsertUser():
    if request.method == 'POST':
        executionState:bool = False
        cur = get_db().cursor()
        data =request.get_json(force= True)
        try:
            date_created = datetime.datetime.now()
            is_active = 1
            hash_password = pwd_context.hash(data['hashed_password'])
            cur.execute( "INSERT INTO users ( user_name, hashed_password, full_name, email_id, date_created, is_active ) VALUES (:user_name, :hashed_password, :full_name, :email_id, :date_created, :is_active)",
            {"user_name":data['user_name'], "hashed_password":hash_password, "full_name":data['full_name'], "email_id":data['email_id'], "date_created":date_created,"is_active":is_active})
            if(cur.rowcount >=1):
                executionState = True
            get_db().commit()

        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data Instersted Sucessfully"), 201
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
            hash_password = pwd_context.hash(data['hashed_password'])
            cur.execute("UPDATE users SET hashed_password=? WHERE user_name=? AND EXISTS(SELECT 1 FROM users WHERE user_name=? AND is_active=1)", (hash_password, uid,uid))
            if(cur.rowcount >=1):
                executionState = True
                get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Updated SucessFully"), 201
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
            cur.execute("UPDATE users SET is_active =? WHERE user_name=? AND EXISTS(SELECT 1 FROM users WHERE user_name=? AND is_active=1)", (0,uid,uid))

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
    app.run(debug=True, port=5001)
