from flask import Flask, request
from flask import jsonify
import json
import sqlite3
from datetime import datetime


app = Flask(__name__)

@app.route('/comment', methods = ['POST'])

def post():
    #conn = sqlite3.connect('example.db')
    #c = conn.cursor()
    if request.method == 'POST':
        data = request.get_json(force=True)
        #c.execute("INSERT INTO post_article VALUES (:aid,:atext,:atitle,:aut,:atcreate,:atmod)",{'aid':id,'atext':text,'atitle':title,'aut':author,'atcreate':tcreate,'atmod':tmod})
        #conn.commit()
    #conn.close()
        comments = data['comment']
        article_id = data['art_id']
        tag_id  = data['tag_ID']
        comment_id = data['comment_ID']
    return '''
           The comment is: {}
           The article is: {}
           The tage is: {}
           The comment_id is: {}'''.format(comments, article_id,tag_id, comment_id)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
