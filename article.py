from flask import Flask,request, g
from flask import jsonify
import json
from flask import g
import sqlite3
import datetime
from DatabaseInstance import get_db
from authentication import *

app = Flask(__name__)

#insert articles
@app.route('/article',methods = ['POST'])
@requires_auth
def insertarticle():
    if request.method == 'POST':
        data = request.get_json(force = True)
        executionState:bool = False
        try:
            cur = get_db().cursor()
            current_time= datetime.datetime.now()
            is_active_article=1
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("INSERT INTO article(title,author,content,date_created,date_modified,is_active_article) VALUES (:title, :author, :content, :date_created, :date_modified, :is_active_article)",{"title":data['title'],"author":uid,"content": data['content'], "date_created":current_time,"date_modified":current_time,"is_active_article":is_active_article })
            last_inserted_row = cur.lastrowid
            url_article=("http://127.0.0.1:5000/article/"+str(last_inserted_row)+"")
            cur.execute("UPDATE article set url=? where article_id=?",(url_article,last_inserted_row))
            if(cur.rowcount >=1):
                    executionState = True
            get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data Instersted Sucessfully"), 200
            else:
                return jsonify(message="Failed to insert data"), 409


#cur.execute("UPDATE post_article set art=?,lmod_time=? where id=?", (data['art'],tmod,data['id']))

#get latest n article and get all article
@app.route('/article',methods = ['GET'])
def latestArticle():
    if request.method == 'GET': # try except
        limit = request.args.get('limit')
        article_id = request.args.get('article_id')
        metadata = request.args.get('metadata')
        executionState:bool = True
        cur = get_db().cursor()
        print(metadata)
        try:
            if limit is not None :
                cur.execute("select * from article  where is_active_article = 1 order by date_created desc limit :limit",  {"limit":limit})
                row = cur.fetchall()
                if list(row) == []:
                    return "No such value exists\n"
                return jsonify(row)

            if limit is None and article_id is None and metadata is None:
                cur.execute('''Select * from article''')
                row = cur.fetchall()
                if list(row) == []:
                    return "No such value exists\n"
                return jsonify(row)

            if article_id is not None:
                cur.execute("SELECT * from  article WHERE article_id="+article_id)
                row = cur.fetchall()
                if list(row) == []:
                    return "No such value exists\n"
                return jsonify(row)

            if metadata is not None:
                cur.execute("select title,author,date_created,date_modified from article  where is_active_article = 1 order by date_created desc limit :metadata", {"metadata":metadata})
                row = cur.fetchall()
                if list(row) == []:
                    return "No such value exists\n"
                return jsonify(row)

        except:
            get_db().rollback()
            executionState = False
        finally:
            if executionState == False:
                return jsonify(message="Fail to retrive from db"), 409
            else:
                return jsonify(row)

# update article

@app.route('/article',methods = ['PUT'])
@requires_auth
def updateArticle():
    if request.method == 'PUT':
        executionState:bool = False
        cur = get_db().cursor()
        try:
            data = request.get_json(force = True)

            tmod= datetime.datetime.now()
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("UPDATE article set content=?,date_modified=? where article_id=? and author =?", (data['content'],tmod,data['article_id'], uid))
            if(cur.rowcount >=1):
                executionState = True
            get_db().commit()
        except:
            get_db().rollback()
            print("Error in update")
        finally:
            if executionState:
                return jsonify(message="Updated Article SucessFully"), 200
            else:
                return jsonify(message="Failed to update Article"), 409

#delete article by article id

@app.route('/article', methods = ['DELETE'])
def deleteArticle():
    if request.method == 'DELETE':
        cur = get_db().cursor()
        executionState:bool = False
        try:
            data = request.get_json(force=True)
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("update article set is_active_article=0 where article_id=:article_id and author= :author AND EXISTS(SELECT 1 FROM article WHERE user_name=:author AND is_active_article=1)",{"article_id":data['article_id'], "author":uid})
            row = cur.fetchall()
            if cur.rowcount >= 1:
                executionState = True
            get_db().commit()

        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Deleted Article SucessFully"),200
            else:
                return jsonify(message="Failed to delete Article"),409



if __name__ == '__main__':
    app.run(debug=True, port= 5000)
