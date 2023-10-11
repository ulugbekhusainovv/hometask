# https://dummyjson.com/carts
import psycopg2
from config import password
con = psycopg2.connect(
    dbname='carts',
    user="postgres",
    password=password,
    host="localhost"
)
con.autocommit = True
cursor = con.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS carts(
               id BIGINT PRIMARY KEY NOT NULL,
               products JSON NOT NULL,
               total BIGINT NULL,
               discountedTotal BIGINT NULL,
               userId BIGINT NOT NULL,
               totalProducts BIGINT NULL,
               totalQuantity BIGINT NULL
            )""")
import requests
import json
url = "https://dummyjson.com/carts"
response = requests.get(url=url)
if response.status_code == 200:
    result = response.text
    jsonRes = json.loads(result)
    carts = jsonRes['carts'][:10]
    for cart in carts:
        cartId = cart["id"]
        products = json.dumps(cart["products"])
        total = cart["total"]
        discountedTotal = cart["discountedTotal"]
        userId = cart["userId"]
        totalProducts = cart["totalProducts"]
        totalQuantity = cart["totalQuantity"]
        insert_query = "INSERT INTO carts (id, products, total, discountedTotal, userId, totalProducts, totalQuantity) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (cartId, products,total,discountedTotal,userId,totalProducts,totalQuantity)
        cursor.execute(insert_query , values)
con.commit()
cursor.close()
con.close()