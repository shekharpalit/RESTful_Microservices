import sqlite3
from flask import Flask, request, jsonify, g, Response




app = Flask(__name__)
DATABASE = 'Main.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)  #create a database instance and use it for later execution
        print("database instance is created")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
