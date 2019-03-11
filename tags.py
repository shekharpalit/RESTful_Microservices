from flask import Flask, request
from flask import jsonify
import json
import sqlite3
from datetime import datetime


app = Flask(__name__)


@app.route('/tags',methods = ['GET'])

def getArticlesFromTag():
    if request.method == 'GET':
        data = request.args.get('tag')
        print(len(data))
        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            tmod= datetime.now()
            cur.execute("Select * from article where art_id IN(Select art_id from normTable where tag_ID in (Select tag_id from tags WHERE tag_name =:tag_name ))", {"tag_name":data})
            row = cur.fetchall()
            print(row)
            return jsonify(row)

@app.route('/tags', methods = ['POST'])
def tags():
    if request.method == 'POST':
        data = request.get_json(force=True)

        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            #check if tag exists or not
            cur.execute("INSERT INTO tags VALUES (:tag_ID,:tag_name)",{"tag_ID":5,"tag_name": data['tag_name']})
            tag_ID = cur.lastrowid
            cur.execute("INSERT INTO normTable(tag_ID, art_id) SELECT :tag_ID, art_id FROM article WHERE article_title IN (:article_title)",(tag_ID,data['article_title']))
            return "tags inserted successfully \n"


@app.route('/tags', methods = ['DELETE'])

def deleteTagFromArticle():
    if request.method == 'DELETE':
        tag_name = request.args.get('tag_name')
        art_id = request.args.get('art_id')
        #print(tag_name+art_id)
        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            #check if tag name exists or not
            cur.execute("delete from normTable where tag_ID IN ( Select tag_ID from tags WHERE tag_name =:tag_name) AND art_id=:art_id",{"tag_name":tag_name,"art_id":art_id})
            #check for query result
            conn.commit()
    return "Tag Deleted"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
