from flask import Flask
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

@app.route('/post')
def tpost():
    conn=sqlite3.connect('art.db')
    c=conn.cursor()

    id="10"
    text="this is 10th article"
    title="i am ten"
    author="prakash"
    tcreate="2015-05-22 01:01:01.000"
    tmod="2016-05-22 01:01:01.000"

    c.execute("INSERT INTO post_article VALUES (:aid,:atext,:atitle,:aut,:atcreate,:atmod)",{'aid':id,'atext':text,'atitle':title,'aut':author,'atcreate':tcreate,'atmod':tmod})
    conn.commit()
    conn.close()
    return "Data inserted"

@app.route('/get')
def tget():
    conn=sqlite3.connect('art.db')
    c=conn.cursor()
    c.execute('''Select * from post_article''')
    row = c.fetchall()
    #user = query_db('select * from users where username = ?',[the_username], one=True)
    conn.commit()
    return jsonify(row)

@app.route('/get_latest')
def tget_latest():
    conn=sqlite3.connect('art.db')
    c=conn.cursor()
    c.execute('''select art,time_created from post_article order by time_created desc limit 1''')
    row = c.fetchall()
    #user = query_db('select * from users where username = ?',[the_username], one=True)
    conn.commit()
    return jsonify(row)

@app.route('/art_find/<id>')
def art_find(id):
    conn=sqlite3.connect('art.db')
    c=conn.cursor()
    c.execute("Select * from post_article where id=?",(id))
    row = c.fetchall()
    #user = query_db('select * from users where username = ?',[the_username], one=True)
    conn.commit()
    return jsonify(row)



@app.route('/art_edit/<id>')
def art_edit(id):
    conn=sqlite3.connect('art.db')
    c=conn.cursor()
    text="this was article but modified"
    id=id
    tmod= datetime.now()
    c.execute("UPDATE post_article SET art =:atext,lmod_time=:atmod WHERE ID = :aid",{'aid':id,'atext':text,'atmod':tmod})
    row = c.fetchall()
    #user = query_db('select * from users where username = ?',[the_username], one=True)
    conn.commit()
    return "data edited with current time stamp"






@app.route('/q/<id>')
def query_db(query, args=(), one=False):
    cur = get_db().execute('select * from post_article where id = ?', args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv











@app.route('/')
def hello():
    return "Home"

@app.route('/post/new')
def post_art():


    return json.dumps(Article())


@app.route('/articles')
def articles():

    return json.dumps(Article())

@app.route('/art/<id>')
def artid(id):
    return json.dumps(Articleid(id))

if __name__ == '__main__':
    app.run(debug=True)
