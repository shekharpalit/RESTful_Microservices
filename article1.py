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

    c.execute('''Create table article(article_id integer PRIMARY KEY,title text,author text,content text,date_created text,date_modified text,isActiveArticle  integer,URL text)''')
    conn.commit()
    return "table created"


@app.route('/article',methods = ['POST','PATCH'])
def insertarticle():
    if request.method == 'POST':
        data = request.get_json(force = True)
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            current_time= datetime.datetime.now()
            isActiveArticle=1
            cur.execute("INSERT INTO article(title,author,date_created,date_modified,isActiveArticle,URL) VALUES (:title,:author,:date_created,:date_modified,:isActiveArticle,:URL)",{"title":data['title'],"author":data['author'],"date_created":current_time,"date_modified":current_time,"isActiveArticle":isActiveArticle,"URL":data['URL']})
            tag_ID = cur.lastrowid

            url_article=("http://127.0.0.1:5000/article/"+str(tag_ID)+".")
            cur.execute("UPDATE article set URL=? where article_id=?",(url_article,tag_ID))
    return "DAtA inserted"


            #cur.execute("UPDATE post_article set art=?,lmod_time=? where id=?", (data['art'],tmod,data['id']))


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
'''
@app.route('/article/view',methods = ['GET'])

def Article():
    if request.method == 'GET':
        data = request.args.get('title')
        print(data)
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            tmod= datetime.now()
            cur.execute("select * from post_article where title like :data ", {"data":data})
            row = cur.fetchall()
            conn.commit()
            return jsonify(row)
'''
@app.route('/article1',methods = ['PATCH'])
def updateArticle():
    if request.method == 'PATCH':
        content = request.args.get('content')
        article_id = request.args.get('article_id')
        data = request.get_json(force = True)
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            tmod= datetime.now()
            cur.execute("UPDATE article set content=?,date_modified=? where article_id=?", (data['content'],tmod,data['article_id']))
    return "Rows Updated"

@app.route('/article', methods = ['DELETE'])

def deleteArticle():
    if request.method == 'DELETE':
        article_id = request.args.get('article_id')
        with sqlite3.connect('com.db') as conn:
            cur = conn.cursor()
            cur.execute("delete from post_article where title like ':title')",{"title":data['article_id']})
    return "Article Deleted"










@app.route('/')
def hello():
    return "Home"



if __name__ == '__main__':
    app.run(debug=True)