import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="shopuser",
        password="password123",
        database="ecommerce_db_2"
    )
