from flask import Flask,request
from flask import jsonify
import json
from flask import g
import sqlite3
import datetime
from datetime import datetime
from art import Article,Articleid
app = Flask(__name__)





@app.route('/create')
def tcreate():
    conn=sqlite3.connect('art.db')
    c=conn.cursor()
    c.execute('''Create table post_article(id integer PRIMARY KEY,art text,title text,author text,time_created text,lmod_time text)''')
    conn.commit()
    return "table created"






@app.route('/restarticle',methods = ['GET', 'POST', 'DELETE'])
def tget2():
    if(request.method=='GET'):
        conn=sqlite3.connect('art.db')
        c=conn.cursor()
        c.execute('''Select * from post_article''')
        row = c.fetchall()
        #user = query_db('select * from users where username = ?',[the_username], one=True)
        conn.commit()
        return jsonify(row)
    if(request.method=='POST'):
        conn=sqlite3.connect('art.db')
        c=conn.cursor()

        id=request.form.get('id')
        text=request.form.get('text')
        title=request.form.get('title')
        author=request.form.get('author')
        tcreate=request.form.get('tcreate')
        tmod=request.form.get('tmod')

        c.execute("INSERT INTO post_article VALUES (:aid,:atext,:atitle,:aut,:atcreate,:atmod)",{'aid':id,'atext':text,'atitle':title,'aut':author,'atcreate':tcreate,'atmod':tmod})
        conn.commit()
        conn.close()
        return "Data inserted"

    if(request.method=='DELETE'):
        conn=sqlite3.connect('art.db')
        c=conn.cursor()
        tmod= datetime.now()
        id=request.form.get('id')
        sql = 'DELETE FROM post_article WHERE id=?'
        c.execute(sql, (id,))
        conn.commit()
        return "artile deleted"
        


@app.route('/restarticle/sort',methods = ['GET', 'POST', 'DELETE'])
def tget3():
    if(request.method=='POST'):
        conn=sqlite3.connect('art.db')
        c=conn.cursor()
        id=request.form.get('id')
        sql = 'select art,time_created from post_article order by time_created desc limit ?'
        c.execute(sql, (id,))
        row = c.fetchall()
        conn.commit()
        return jsonify(row)




@app.route('/restarticle/edit',methods = ['GET', 'POST', 'DELETE'])
def tget4():
    if(request.method=='POST'):
        conn=sqlite3.connect('art.db')
        c=conn.cursor()
        id=request.form.get('id')
        text=request.form.get('text')
        tmod= datetime.now()
        c.execute("UPDATE post_article SET art =:atext,lmod_time=:atmod WHERE ID = :aid",{'aid':id,'atext':text,'atmod':tmod})
        row = c.fetchall()
        conn.commit()
        return jsonify(row)

@app.route('/restarticle/find',methods = ['GET', 'POST', 'DELETE'])
def tget5():
    if(request.method=='POST'):
        conn=sqlite3.connect('art.db')
        c=conn.cursor()
        id=request.form.get('id')
        sql = 'Select * from post_article where id=?'
        c.execute(sql, (id,))
        row = c.fetchall()
        conn.commit()
        return jsonify(row)



@app.route('/')
def hello():
    return "Home"



if __name__ == '__main__':
    app.run(debug=True)
