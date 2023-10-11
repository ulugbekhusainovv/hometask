import psycopg2
from config import password
con = psycopg2.connect(
    dbname='users',
    user="postgres",
    password=password,
    host="localhost"
)
con.autocommit = True
cursor = con.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               id BIGINT PRIMARY KEY,
               firstName VARCHAR(30) NOT NULL,
               lastName VARCHAR(30) NOT NULL,
               maidenName VARCHAR(20) NULL,
               age SMALLINT NOT NULL,
               gender VARCHAR(10) NOT NULL,
               email VARCHAR(25) NULL,
               phone VARCHAR(20) NOT NULL,
               username VARCHAR(20) NULL,
               password VARCHAR(20) NOT NULL,
               birthDate DATE NOT NULL,
               image VARCHAR(999) NOT NULL
)""")
import requests
import json
url = "https://dummyjson.com/users"
response = requests.get(url=url)
if response.status_code == 200:
    result = response.text
    jsonRes = json.loads(result)
    users = jsonRes['users'][:10]
    for user in users:
        userId = user["id"]
        firstName = user["firstName"]
        lastName = user["lastName"]
        maidenName = user["maidenName"]
        age = user["age"]
        gender = user["gender"]
        email = user["email"]
        phone = user["phone"]
        username = user["username"]
        password = user["password"]
        birthDate = user["birthDate"]
        image = user["image"]
        insert_query = "INSERT INTO users (id, firstName, lastName, maidenName, age, gender, email, phone, username, password, birthDate, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (userId, firstName, lastName, maidenName, age, gender, email, phone,username, password,birthDate,image)
        cursor.execute(insert_query , values)
con.commit()
cursor.close()
con.close()