from flask import Flask, request
from flask import jsonify
import json
import sqlite3
from datetime import datetime


app = Flask(__name__)

@app.route('/comment', methods = ['POST'])

def comment():
    if request.method == 'POST':
        data = request.get_json(force=True)

        with sqlite3.connect('com.db') as conn:
            try:
                cur = conn.cursor()
                tmod = datetime.now()
                cur.execute("INSERT INTO comments (comment, art_id, tag_ID, timestamp) VALUES (:comment, :art_id, :tag_ID, :timestamp) ",{"comment":data['comment'], "art_id":data['art_id'], "tag_ID":data['tag_ID'], "timestamp": tmod})
                return "Comment inserted successfully \n"
            except sqlite3.Error as er:
                print('er:', er.message)
                
@app.route('/comment', methods = ['DELETE'])

def deleteComment():
    if request.method == 'DELETE':
        data = request.args.get('comment_id')
        with sqlite3.connect('com.db') as conn:
            cur = conn.cursor()
            cur.execute("DELETE from comments WHERE comment_ID ="+data)
    return "Deleted Successfully \n"

@app.route('/comment', methods = ['GET'])
def retriveComments():
    if request.method == 'GET':
        data = request.args.get('art_id')
        data1 = request.args.get('number')
        with sqlite3.connect('com.db') as conn:
            if data is not None and data1 is not None:
                cur = conn.cursor()
                dateTime = conn.cursor()
                dateTime.execute("SELECT timestamp, comment FROM(SELECT * FROM comments WHERE art_id="+data+" ORDER BY timestamp DESC LIMIT :data1)",{"data1":data1})
                date = dateTime.fetchall()
                conn.commit()
                return jsonify(date)
            if data is not None and data1 is None:
                data = request.args.get('art_id')
                cur = conn.cursor()
                cur.execute("SELECT comment from comments WHERE art_id ="+data)
                row = cur.fetchall()
                conn.commit()
                return jsonify(row)

@app.route('/comment', methods =['PATCH'])
def retriveNComments():
    if request.method == 'PATCH':
        data = request.get_json(force = True)
        with sqlite3.connect('com.db') as conn:
            cur = conn.cursor()
            tmod = datetime.now()
            cur.execute("UPDATE comments set comment = ?,timestamp=? where art_id =? AND comment_id =?",  (data['comment'],tmod, data['art_id'], data['comment_id']))
    return "Comments modified successfully\n"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
