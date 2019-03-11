from flask import Flask, request, g
from flask import jsonify
import json
import sqlite3
from datetime import datetime


app = Flask(__name__)
DATABASE = 'com.db'

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

#Add comments to the database
@app.route('/comment', methods = ['POST'])
def AddComment():
    if request.method == 'POST':
        executionState:bool = False
        cur = get_db().cursor()
        try:
            data = request.get_json(force=True)
            tmod = datetime.now()
            cur.execute("INSERT INTO comments (comment, art_id, tag_ID, timestamp) VALUES (:comment, :art_id, :tag_ID, :timestamp) ",{"comment":data['comment'], "art_id":data['art_id'], "tag_ID":data['tag_ID'], "timestamp": tmod})
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
def deleteComment():
    if request.method == 'DELETE':
        executionState:bool = False
        cur = get_db().cursor()
        try:
            data = request.args.get('comment_id')
            cur.execute("DELETE from comments WHERE comment_ID ="+data)
            get_db().commit()
            if cur.rowcount >= 1:
                executionState = True
        except:
            get_db().rollback() #if it fails to execute rollback the database
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
@app.route('/comment', methods =['PATCH'])
def UpdateComments():
    if request.method == 'PATCH':
        executionState:bool = False
        cur = get_db().cursor()
        try:
            data = request.get_json(force = True)
            tmod = datetime.now()
            cur.execute("UPDATE comments set comment = ?,timestamp=? where art_id =? AND comment_id =?",  (data['comment'],tmod, data['art_id'], data['comment_id']))
            get_db().commit()
            if cur.rowcount >= 1:
                executionState = True

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
