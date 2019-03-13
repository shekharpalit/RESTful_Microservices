from flask import Flask,request, g
from flask import jsonify
import json
from flask import g
import sqlite3
import datetime
import datetime


app = Flask(__name__)



@app.route('/create')
def tcreate():
    conn=sqlite3.connect('art.db')
    c=conn.cursor()
    c.execute('''Create table article(article_id integer PRIMARY KEY,title text,author text,content text,date_created text,date_modified text,isActiveArticle  integer,url text)''')
    conn.commit()
    return "table created"

#insert articles
@app.route('/article',methods = ['POST'])
def insertarticle():
    if request.method == 'POST':
        data = request.get_json(force = True)
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            current_time= datetime.datetime.now()
            isActiveArticle=1
            cur.execute("INSERT INTO article(title,author,date_created,date_modified,isActiveArticle,url) VALUES (:title,:author,:date_created,:date_modified,:isActiveArticle,:URL)",{"title":data['title'],"author":data['author'],"date_created":current_time,"date_modified":current_time,"isActiveArticle":isActiveArticle,"URL":data['URL']})
            author_ID = cur.lastrowid
            url_article=("http://127.0.0.1:5000/article/"+str(author_ID)+"")
            cur.execute("UPDATE article set URL=? where article_id=?",(url_article,author_ID))
    return "DAtA inserted"


#cur.execute("UPDATE post_article set art=?,lmod_time=? where id=?", (data['art'],tmod,data['id']))

#get latest n article and get all article
@app.route('/article',methods = ['GET'])
def latestArticle():
    if request.method == 'GET':
        data = request.args.get('limit')
        data1 = request.args.get('number')
        with sqlite3.connect('art.db') as conn:
            if data is not None :
                cur = conn.cursor()
                cur.execute("select * from article  where isActiveArticle = 1 order by date_created desc limit :data",  {"data":data})
                row = cur.fetchall()
                conn.commit()
                return jsonify(row)

        #limit = request.args.get('limit')
            if data is None and data1 is None:
                cur = conn.cursor()
                cur.execute('''Select * from article''')
                #cur.execute("select art,time_created from post_article order by time_created desc limit "+data)
                row = cur.fetchall()
                conn.commit()
                return jsonify(row)

#get article from url...article id needed
@app.route('/article/<string:art_id>',methods = ['GET'])
def getTagsFromArticle(art_id):
    if request.method == 'GET':
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            article_id=art_id
            sql=("SELECT * from  article WHERE article_id="+article_id)
            cur.execute(sql)
            row = cur.fetchall()
            return jsonify(row)

# get single article by name.....multiple url /article same get method

@app.route('/article/find',methods = ['GET'])
def Article():
    if request.method == 'GET':
        data = request.args.get('title')
        print(data)
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            cur.execute("select * from article where title like :data ", {"data":data})
            row = cur.fetchall()
            conn.commit()
            return jsonify(row)


# update article

@app.route('/article',methods = ['PATCH'])
def updateArticle():
    if request.method == 'PATCH':
        data = request.get_json(force = True)
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            tmod= datetime.datetime.now()
            cur.execute("UPDATE article set content=?,date_modified=? where article_id=?", (data['content'],tmod,data['article_id']))
    return "Rows Updated"


#delete article by article id

@app.route('/article', methods = ['DELETE'])
def deleteArticle():
    if request.method == 'DELETE':
        article_id = request.args.get('article_id')
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            cur.execute("delete from article where article_id=:article_id",{"article_id":article_id})
            row = cur.fetchall()
            conn.commit()
    return "Article Deleted"



@app.route('/')
def hello():
    return "Home"



if __name__ == '__main__':
    app.run(debug=True)
