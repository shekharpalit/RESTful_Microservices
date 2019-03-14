from flask import Flask, request
from flask import jsonify
import json
from datetime import datetime
from DatabaseInstance import get_db
from authentication import *


app = Flask(__name__)


AuthState = True
def check_auth(username, password):
    cur = get_db().cursor().execute("SELECT user_name, hashed_password from users WHERE user_name=?", (username,))
    row = cur.fetchall()
    if row[0][0] == username and pwd_context.verify(password,row[0][1]):
        return True
    else:
        return False

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

isAuthenticated = True
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.authorization:
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            if not uid or not pwd or check_auth(uid, pwd) == False:
                return authenticate()
            else:
                return f(*args, **kwargs)

        else:
            global isAuthenticated
            isAuthenticated = False
            return f(*args, **kwargs)

    return decorated


#Add comments to the database
@app.route('/comment', methods = ['POST'])
@requires_auth
def AddComment():
    if request.method == 'POST':
        executionState:bool = False
        cur = get_db().cursor()
        data = request.get_json(force=True)
        try:
            if  isAuthenticated == False:
                time_created = datetime.now()
                cur.execute("INSERT INTO comments (comment, user_name, article_id, timestamp) VALUES (:comment, :user_name,:article_id, :timestamp) ",{"comment":data['comment'], "user_name":"Anonymous Coward", "article_id":data['article_id'], "timestamp": time_created})
                get_db().commit()
                if cur.rowcount >= 1:
                    executionState = True
            else:
                uid = request.authorization["username"]
                pwd = request.authorization["password"]
                time_created = datetime.now()
                cur.execute("INSERT INTO comments (comment, user_name, article_id, timestamp) VALUES (:comment, :user_name,:article_id, :timestamp) ",{"comment":data['comment'], "user_name":uid, "article_id":data['article_id'], "timestamp": time_created})
                get_db().commit()
                if cur.rowcount >= 1:
                    executionState = True

        except:
            get_db().rollback()   #if it fails to execute rollback the database
            executionState = False
        finally:
            if executionState:
                return jsonify(message="Passed"), 201
            else:
                return jsonify(message="Fail"), 409    #use 409 if value exists and send the message of conflict

#delete a comment from the database
@app.route('/comment', methods = ['DELETE'])
@requires_auth
def deleteComment():
    if request.method == 'DELETE':
        executionState:bool = False
        cur = get_db().cursor()
        try:
            data = request.args.get('comment_id')
            cur.execute("SELECT user_name FROM comments WHERE comment_id="+data)
            row = cur.fetchall()
            if row[0][0] == "Anonymous Coward":
                cur.execute("DELETE from comments WHERE user_name ='Anonymous Coward' AND comment_id="+data)
                if cur.rowcount >= 1:
                    executionState = True
                get_db().commit()
            if  isAuthenticated == True:
                uid = request.authorization["username"]
                pwd = request.authorization["password"]
                if row[0][0] == uid:
                    cur.execute("DELETE from comments WHERE user_name=? AND comment_id=?",(uid,data))
                    if cur.rowcount >= 1:
                        executionState = True
                    get_db().commit()
        except:
            get_db().rollback()                  #if it fails to execute rollback the database
            executionState = False
        finally:
            if executionState:
                return jsonify(message="Passed"), 201
            else:
                return jsonify(message="Fail"), 409

#retrive all or n number of comments from the database
@app.route('/comment', methods = ['GET'])
def retriveComments():
    if request.method == 'GET':
        executionState:bool = False
        cur = get_db().cursor()
        try: #move the try block after the below for test case if the data is none or not then only try db connection
            data = request.args.get('art_id')
            data1 = request.args.get('number')
            executionState = True

            if data is not None and data1 is not None:
                cur.execute("SELECT timestamp, comment FROM(SELECT * FROM comments WHERE art_id="+data+" ORDER BY timestamp DESC LIMIT :data1)",{"data1":data1})
                retriveNcomments = cur.fetchall()
                get_db().commit()
                if list(retriveNcomments) == []:
                    return "No such value exists\n"
                return jsonify(retriveNcomments)

            if data is not None and data1 is None:
                cur.execute("SELECT comment from comments WHERE art_id ="+data)
                retriveAllComments = cur.fetchall()
                get_db().commit()
                if list(retriveAllComments) == []:
                    return "No such value exists\n"
                return jsonify(retriveAllComments)
        except:
            get_db().rollback() #if it fails to execute rollback the database
            executionState = False

        finally:
            if executionState == False:
                return jsonify(message="Fail"), 409

#Update the comments in the database for a particular user
@app.route('/comment', methods =['PUT'])
@requires_auth
def UpdateComments():
    if request.method == 'PUT':
        executionState:bool = False
        cur = get_db().cursor()
        try:
            data = request.get_json(force = True)
            cur.execute("SELECT user_name FROM comments WHERE comment_id=?",(data['comment_id']))
            row = cur.fetchall()
            timeCreated = datetime.now()
            if row[0][0] == "Anonymous Coward":
                cur.execute("UPDATE comments set comment = ?,timestamp=? where user_name = 'Anonymous Coward' AND comment_id =?", (data['comment'],timeCreated, data['comment_id']))
                if cur.rowcount >= 1:
                    executionState = True
                get_db().commit()
            if  isAuthenticated == True:
                uid = request.authorization["username"]
                pwd = request.authorization["password"]
                if row[0][0] == uid:
                    cur.execute("UPDATE comments set comment = ?,timestamp=? where user_name =? AND comment_id =?",  (data['comment'],timeCreated, uid, data['comment_id']))
                    if cur.rowcount >= 1:
                        executionState = True
                    get_db().commit()
        except:
            get_db().rollback() #if it fails to execute rollback the database
            executionState = False

        finally:
            if executionState:
                return jsonify(message="Passed"), 201
            else:
                return jsonify(message="Fail"), 409

if __name__ == '__main__':
    app.run(debug=True, port=5000)
