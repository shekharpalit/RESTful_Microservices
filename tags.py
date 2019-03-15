from flask import Flask, request
from flask import jsonify
import json
import sqlite3
from datetime import datetime
from DatabaseInstance import get_db

app = Flask(__name__)


@app.route('/tags',methods = ['GET'])
def getArticlesFromTag():
    if request.method == 'GET':
        data = request.args.get('tag')
        cur = get_db().cursor()
        tmod= datetime.now()
        print("here")
        cur.execute("Select * from article where article_id IN(Select article_id from tag_article_mapping where tag_id in (Select tag_id from tags WHERE tag_name =:tag_name ))", {"tag_name":data})
        row = cur.fetchall()
        if len(row) ==0:
            return "No articles containing the tags", 204
        else:
            return jsonify(row),200

#get tags from the url utility
@app.route('/tags/<string:article_id>',methods = ['GET'])
def getTagsFromArticle(article_id):
    if request.method == 'GET':
        cur = get_db().cursor()
        cur.execute("SELECT tag_name from tags WHERE tag_id IN (SELECT tag_id from tag_article_mapping WHERE article_id=:article_id )", {"article_id":article_id})
        row = cur.fetchall()
        return jsonify(row),200


@app.route('/tags', methods = ['POST'])
def addTagstoArticle():
    if request.method == 'POST':
        data = request.get_json(force=True)
        executionState:bool = False
        print(str(data))
        cur = get_db().cursor()
        try:
            #check if tag exists or not
            #check if the article exists or not
            cur.execute("SELECT * FROM article WHERE article_id=:article_id",{"article_id":data['article_id']})
            articleExists = cur.fetchall()
            if articleExists != ():
                cur.execute("INSERT INTO tags(tag_name) VALUES (:tag_name)",{"tag_name": data['tag_name']})
                tag_id = cur.lastrowid
                cur.execute("INSERT INTO tag_article_mapping(tag_id, article_id) VALUES(:tag_id, :article_id) ",{"tag_id":tag_id,"article_id":data['article_id']})
                if (cur.rowcount >=1):
                    executionState =True
                get_db().commit()
            if articleExists ==():
                return jsonify(message="Article does not exist"),409
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Tag inserted successfully \n"),201
            else:
                return jsonify(message="Failed to insert tag"),409


#adding a new and existing tag to the article
@app.route('/tags', methods = ['PUT'])
def addTagsToExistingArticle():
    if request.method == 'PUT':
        data = request.get_json(force=True)
        tags =data['tags']
        #return 204 if not found
        print(tags)
        executionState:bool = False
        try:
            for tag in tags:
                    cur = get_db().cursor()
                    cur.execute("SELECT tag_id FROM tags WHERE tag_name=:tag_name",{"tag_name":tag})
                    result = cur.fetchone()
                    if str(result)!="None":
                        tag_id =str(result[0])
                        #add the new tag here
                        #insert the relation if not exists
                        cur.execute("INSERT INTO tag_article_mapping(tag_id, article_id) SELECT (:tag_id),(:article_id) WHERE NOT EXISTS(SELECT 1 FROM tag_article_mapping WHERE tag_id= :tag_id  AND article_id = :article_id)", {"tag_id":tag_id, "article_id":data['article_id']})
                    elif str(result)=="None":

                        cur.execute("INSERT INTO tags(tag_name) VALUES( :tag_name )",{"tag_name":tag})
                        new_tag_inserted_id =cur.lastrowid
                        cur.execute("INSERT INTO tag_article_mapping (tag_id, article_id) VALUES (:tag_id, :article_id)",{"tag_id":new_tag_inserted_id,"article_id":data['article_id']})
            if (cur.rowcount >=1):
                executionState =True
            get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Added Tags to an existing article"),201
            else:
                return jsonify(message="Failed to add tags to the article"),409



@app.route('/tags', methods = ['DELETE'])
def deleteTagFromArticle():
    if request.method == 'DELETE':
        data = request.get_json(force=True)
        #article_id = request.args.get('article_id')
        #print(tag_name+article_id)
        executionState:bool = False
        cur = get_db().cursor()
        try:
            cur.execute("SELECT article_id FROM article WHERE article_id=:article_id",{"article_id":data['article_id']})
            result = cur.fetchone()
            if str(result)!="None":
                #check if tag name exists or not
                cur.execute("DELETE from tag_article_mapping where tag_id IN ( Select tag_id from tags WHERE tag_name =:tag_name) AND article_id=:article_id",{"tag_name":data['tag_name'],"article_id":data['article_id']})
                #check for query result
                if (cur.rowcount >=1):
                    executionState =True
                get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Deleted Tag SucessFully"),200
            else:
                return jsonify(message="Failed to delete tags from article"),409



if __name__ == '__main__':
    app.run(debug=True, port = 5003)
