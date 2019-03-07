from flask import Flask, request
import sqlite3
from user import User

app = Flask(__name__)
conn = sqlite3.connect('test_user.db')
c =conn.cursor()


#create user
@app.route('/user', methods=['POST'])
def about():
    if request.method == 'POST':
        userData = request.get_json()
        # write something for hashed password
        # sending hardcoded 1 for active users
        # write something for current data
        # BASIC AUTHENTICATION MODULE IMPLEMENTATION
        with conn:
            c.execute("INSERT INTO users VALUES (:user_name,:hash_pwd,:name, :email_id, :date_created, :is_active )",
             {'user_name':userData`.user_name, 'hash_pwd':userData.hash_pwd, 'name':emp.name, 'email_id':userData.email_id, 'date_created':userData.date_created
             'is_active':1})
             #return status code of query execution

#update user
@app.route('/user', methods=['PUT'])
def articles():
    if request.method == 'POST':
        userData = request.get_json()
        #get something here for changing password
        with conn:
            c.execute("""UPDATE users SET name=:name, email_id:email_id, hash_pwd:hash_pwd
                        WHERE id:= id """, {'name':userData.first, 'email_id':userData.email_id, 'hash_pwd':hash_pwd})


#delete user
@app.route('/user', methods=['DELETE'])
def article(id):
    #BASIC AUTHENTICATION FOR DELETE
    return render_template('article.html',  id=id)

if __name__== "__main__":
    app.run(debug =True)
