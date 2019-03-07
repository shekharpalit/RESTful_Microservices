import sqlite3

conn = sqlite3.connect('./Main.db', timeout=10)
print("Successfully connected")

conn.execute('CREATE TABLE if not exists users (user_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT NOT NULL,  hash_pwd TEXT NOT NULL, name TEXT NOT NULL, email_id TEXT NOT NULL,  date_created DATE NOT NULL, is_active INTEGER NOT NULL)')
#conn.execute('CREATE TABLE if not exists article (art_id INTEGER PRIMARY KEY NOT NULL, user_id INTEGER NOT NULL, articles TEXT NOT NULL, isActiveArticle TEXT, timeCreated INTEGER, timeModified INTEGER, FOREIGN KEY (user_id) REFERENCES users(user_id))')
#conn.execute('CREATE TABLE if not exists tags (tag_name TEXT, tag_ID INTEGER PRIMARY KEY NOT NULL')
##conn.execute('CREATE TABLE if not exists normTable (tag_ID INTEGER, art_id INTEGER, FOREIGN KEY (art_id) REFERENCES article(art_id), FOREIGN KEY (tag_ID) REFERENCES tags(tag_ID))')
print ("Table created successfully")
conn.close()
#CREATE TABLE if not exists comments (comment_ID INTEGER PRIMARY KEY, comment TEXT, art_id INTEGER, tag_ID INTEGER, timestamp INTEGER, FOREIGN KEY (art_id) REFERENCES article(art_id), FOREIGN KEY (tag_ID) REFERENCES tags(tag_ID))
