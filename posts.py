# https://dummyjson.com/posts
import psycopg2
from config import password
con = psycopg2.connect(
    dbname='posts',
    user="postgres",
    password=password,
    host="localhost"
)
con.autocommit = True
cursor = con.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS posts(
               id BIGINT PRIMARY KEY NOT NULL,
               title VARCHAR(50) NULL,
               body TEXT NULL,
               userId BIGINT NOT NULL,
               tags JSON NULL,
               reactions BIGINT NULL
            )""")
import requests
import json
url = "https://dummyjson.com/posts"
response = requests.get(url=url)
if response.status_code == 200:
    result = response.text
    jsonRes = json.loads(result)
    posts = jsonRes['posts'][:10]
    for post in posts:
        postId = post["id"]
        title = post["title"]
        body = post["body"]
        userId = post["userId"]
        tags = json.dumps(post["tags"])
        reactions = post["reactions"]
        insert_query = "INSERT INTO posts (id, title, body, userId, tags, reactions) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (postId,title,body,userId,tags,reactions)
        cursor.execute(insert_query , values)
con.commit()
cursor.close()
con.close()