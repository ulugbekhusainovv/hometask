# https://dummyjson.com/comments
import psycopg2
from config import password
con = psycopg2.connect(
    dbname='comments',
    user="postgres",
    password=password,
    host="localhost"
)
con.autocommit = True
cursor = con.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS comments(
               id BIGINT PRIMARY KEY NOT NULL,
               body TEXT NULL,
               postId BIGINT NOT NULL,
               comment_user JSON NULL
            )""")
import requests
import json
url = "https://dummyjson.com/comments"
response = requests.get(url=url)
if response.status_code == 200:
    result = response.text
    jsonRes = json.loads(result)
    comments = jsonRes['comments'][:10]
    json_string = json.dumps(comments)
    for comment in comments:
        commentId = comment["id"]
        body = comment["body"]
        postId = comment["postId"]
        user = json.dumps(comment["user"])
        insert_query = "INSERT INTO comments (id, body, postId,comment_user) VALUES (%s, %s, %s, %s)"
        values = (commentId,body,postId,user)
        cursor.execute(insert_query , values)
con.commit()
cursor.close()
con.close()