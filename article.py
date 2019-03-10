from flask import Flask,request
from flask import jsonify
import json
from flask import g
import sqlite3
import datetime
from datetime import datetime


app = Flask(__name__)



@app.route('/create')
def tcreate():
    conn=sqlite3.connect('art.db')
    c=conn.cursor()
    c.execute('''Create table post_article(id integer PRIMARY KEY,art text,title text,author text,time_created text,lmod_time text)''')
    conn.commit()
    return "table created"



@app.route('/article',methods = ['POST'])
def insertarticle():
    if request.method == 'POST':
        data = request.get_json(force = True)
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            tmod= datetime.now()
            cur.execute("INSERT INTO post_article VALUES (:aid,:atext,:atitle,:aut,:atcreate,:atmod)",
            'aid':data['aid'],'atext':data['atext'],'atitle':data['atitle'],'aut':data['aut'],'atcreate':data['tcreate'],'atmod':tmod})
            #cur.execute("UPDATE post_article set art=?,lmod_time=? where id=?", (data['art'],tmod,data['id']))
    return "DAtA inserted"


@app.route('/article',methods = ['GET'])
def latestarticle():
    if request.method == 'GET':
        data = request.args.get('art_id')
        data1 = request.args.get('number')
        with sqlite3.connect('art.db') as conn:
            if data is not None :
                '''return "first one"
'''
                cur = conn.cursor()
                tmod= datetime.now()
                cur.execute("select * from post_article order by time_created desc limit :data",  {"data":data})
                row = cur.fetchall()
                conn.commit()
                return jsonify(row)

        #limit = request.args.get('limit')
            if data is None and data1 is None:
                cur = conn.cursor()
                cur.execute('''Select * from post_article''')
                #cur.execute("select art,time_created from post_article order by time_created desc limit "+data)
                row = cur.fetchall()
                conn.commit()
                return jsonify(row)


@app.route('/article',methods = ['PATCH'])
def updatearticle():
    if request.method == 'PATCH':
        data = request.get_json(force = True)
        with sqlite3.connect('art.db') as conn:
            cur = conn.cursor()
            tmod= datetime.now()
            cur.execute("UPDATE post_article set art=?,lmod_time=? where id=?", (data['art'],tmod,data['id']))
    return "Rows Updated"












@app.route('/')
def hello():
    return "Home"



if __name__ == '__main__':
    app.run(debug=True)
