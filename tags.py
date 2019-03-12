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
        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            tmod= datetime.now()
            cur.execute("Select * from article where art_id IN(Select art_id from normTable where tag_ID in (Select tag_id from tags WHERE tag_name =:tag_name ))", {"tag_name":data})
            row = cur.fetchall()
            return jsonify(row)

#get tags from the url utility
@app.route('/tags/<string:art_id>',methods = ['GET'])
def getTagsFromArticle(art_id):
    if request.method == 'GET':
        with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT tag_name from tags WHERE tag_ID IN (SELECT tag_ID from normTable WHERE art_id=:art_id )", {"art_id":art_id})
            row = cur.fetchall()
            return jsonify(row)


@app.route('/tags', methods = ['POST'])
def tags():
    if request.method == 'POST':
        data = request.get_json(force=True)
        executionState:bool = False
        try:
            with sqlite3.connect('tags.db') as conn:
            cur = conn.cursor()
            #check if tag exists or not
            cur.execute("INSERT INTO tags VALUES (:tag_ID,:tag_name)",{"tag_ID":5,"tag_name": data['tag_name']})
            tag_ID = cur.lastrowid
            cur.execute("INSERT INTO normTable(tag_ID, art_id) SELECT :tag_ID, art_id FROM article WHERE article_title IN (:article_title)",(tag_ID,data['article_title']))
            if (cur.rowcount >=1):
                executionState =True
            conn.commit()
        except sqlite3.Error as er:
            conn.rollback()
            print("Error:")
            print(er.message)
        finally:
            if executionState:
                return jsonify(message="Tags inserted successfully \n"),201
            else:
                return jsonify(message="Failed to insert tags"),409


#adding a new and existing tag to the article
@app.route('/tags', methods = ['PUT'])
def addTagsToExistingArticle():
    if request.method == 'PUT':
        data = request.get_json(force=True)
        tags =data['tags']
        #return 204 if not found
        executionState:bool = False
        try:
            for tag in tags:
                    with sqlite3.connect('tags.db') as conn:
                        cur = conn.cursor()
                        cur.execute("SELECT tag_ID FROM tags WHERE tag_name=:tag_name",{"tag_name":tag})
                        result = cur.fetchone()
                        if str(result)!="None":
                            tag_id =str(result[0])
                            #add the new tag here
                            #insert the relation if not exists
                            cur.execute("INSERT INTO normTable(tag_ID, art_id) SELECT (:tag_id),(:art_id) WHERE NOT EXISTS(SELECT 1 FROM normTable WHERE tag_ID= :tag_id  AND art_id = :art_id)", {"tag_id":tag_id, "art_id":data['art_id']})
                        elif str(result)=="None":
                            cur.execute("INSERT INTO tags(tag_name) VALUES(:tag_name)",{"tag_name":tag})
                            new_tag_inserted_id =cur.lastrowid
                            cur.execute("INSERT INTO normTable(tag_ID, art_id)VALUES(:tag_ID, :art_id)",{"tag_ID":new_tag_inserted_id,"art_id":data['art_id']})
        except sqlite3.Error as er:
            conn.rollback()
            print("Error:")
            #print(er.args[0])
            print(er.message)
        finally:
            if executionState:
                return jsonify(message="Added Tags to an existing article"),201
            else:
                return jsonify(message="Failed to add tags to the article"),409



@app.route('/tags', methods = ['DELETE'])
def deleteTagFromArticle():
    if request.method == 'DELETE':
        tag_name = request.args.get('tag_name')
        art_id = request.args.get('art_id')
        #print(tag_name+art_id)
        try:
            with sqlite3.connect('tags.db') as conn:
                cur = conn.cursor()
                #check if tag name exists or not
                cur.execute("delete from normTable where tag_ID IN ( Select tag_ID from tags WHERE tag_name =:tag_name) AND art_id=:art_id",{"tag_name":tag_name,"art_id":art_id})
                #check for query result
                conn.commit()
        except sqlite3.Error as er:
            conn.rollback()
            print("Error:")
            print(er.message)
        finally:
            if executionState:
                return jsonify(message="Deleted Tag SucessFully"),200
            else:
                return jsonify(message="Failed to delete tags from article"),409



if __name__ == '__main__':
    app.run(debug=True)
