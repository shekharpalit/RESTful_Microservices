import sqlite3

conn = sqlite3.connect('./Main.db', timeout=10)
print("Successfully connected")
import sqlite3

conn = sqlite3.connect('./Main.db', timeout=10)
print("Successfully connected")

conn.execute('CREATE TABLE if not exists users (user_name TEXT PRIMARY KEY NOT NULL,  hashed_password TEXT NOT NULL, full_name TEXT NOT NULL, email_id TEXT NOT NULL,  date_created DATE NOT NULL, is_active INTEGER NOT NULL)')
conn.execute('CREATE TABLE if not exists article (article_id INTEGER PRIMARY KEY NOT NULL, title TEXT, author INTEGER NOT NULL, content TEXT NOT NULL, isActiveArticle TEXT, date_created INTEGER, date_modified INTEGER, url TEXT, FOREIGN KEY (author) REFERENCES users(user_name))')
conn.execute('CREATE TABLE if not exists tags (tag_id INTEGER PRIMARY KEY NOT NULL, tag_name TEXT)')
conn.execute('CREATE TABLE if not exists tag_article_mapping (tag_id INTEGER, article_id INTEGER, FOREIGN KEY (article_id) REFERENCES article(article_id), FOREIGN KEY (tag_id) REFERENCES tags(tag_id))')
conn.execute('CREATE TABLE if not exists comments (comment_id INTEGER PRIMARY KEY, comment TEXT, article_id INTEGER, tag_id INTEGER, timestamp INTEGER, FOREIGN KEY (article_id) REFERENCES article(article_id), FOREIGN KEY (tag_id) REFERENCES tags(tag_ID)')
print ("Table created successfully")
conn.close()

#old_ database queries is as follows
'''
conn.execute('CREATE TABLE if not exists users (user_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT NOT NULL,  hash_pwd TEXT NOT NULL, name TEXT NOT NULL, email_id TEXT NOT NULL,  date_created DATE NOT NULL, is_active INTEGER NOT NULL)')
#conn.execute('CREATE TABLE if not exists article (art_id INTEGER PRIMARY KEY NOT NULL, article_title TEXT, user_id INTEGER NOT NULL, articles TEXT NOT NULL, isActiveArticle TEXT, timeCreated INTEGER, timeModified INTEGER, FOREIGN KEY (user_id) REFERENCES users(user_id))')
#conn.execute('CREATE TABLE if not exists tags (tag_ID INTEGER PRIMARY KEY NOT NULL, tag_name TEXT)')
##conn.execute('CREATE TABLE if not exists normTable (tag_ID INTEGER, art_id INTEGER, FOREIGN KEY (art_id) REFERENCES article(art_id), FOREIGN KEY (tag_ID) REFERENCES tags(tag_ID))')
print ("Table created successfully")
conn.close()
#CREATE TABLE if not exists comments (comment_ID INTEGER PRIMARY KEY, comment TEXT, art_id INTEGER, tag_ID INTEGER, timestamp INTEGER, FOREIGN KEY (art_id) REFERENCES article(art_id), FOREIGN KEY (tag_ID) REFERENCES tags(tag_ID))
'''
