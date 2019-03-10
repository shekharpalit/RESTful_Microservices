from flask import Flask, request
from flask import jsonify
import json
import sqlite3
from datetime import datetime


app = Flask(__name__)

@app.route('/tags', methods = ['POST'])

def tags():
    if request.method == 'POST':
        data = request.get_json(force=True)

        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO tags VALUES (:tag_ID,:tag_name)",{"tag_ID":5,"tag_name": data['tag_name']})
            tag_ID = cur.lastrowid
            cur.execute("INSERT INTO normTable(tag_ID, art_id) SELECT :tag_ID, art_id FROM article WHERE article_title IN (:article_title)",(tag_ID,data['article_title']))
            return "tags inserted successfully \n"

'''
@app.route('/tags', methods = ['DELETE'])

def deleteComment():
    if request.method == 'DELETE':
        data = request.args.get('comment_id')
        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            cur.execute("DELETE from comments WHERE comment_ID ="+data)
    return "Deleted Successfully \n"

@app.route('/tags', methods = ['GET'])
def retriveComments():
    if request.method == 'GET':
        data = request.args.get('art_id')
        data1 = request.args.get('number')
        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            dateTime = conn.cursor()
            dateTime.execute("SELECT timestamp, comment FROM(SELECT * FROM comments WHERE art_id="+data+" ORDER BY timestamp DESC LIMIT 3) T1 ORDER BY comment")
            date = dateTime.fetchall()
        return jsonify(date)

'SELECT * FROM distro WHERE id IN (%s)' %
                           ','.join('?'*len(desired_ids)), desired_ids)


@app.route('/tags', methods =['PATCH'])
def retriveNComments():
    if request.method == 'PATCH':
        data = request.get_json(force = True)
        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            tmod = datetime.now()
            cur.execute("UPDATE comments set comment = ?,timestamp=? where art_id =? AND comment_id =?",  (data['comment'],tmod, data['art_id'], data['comment_id']))
    return "Comments modified successfully\n"
'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
