import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from exception import customException
import sys

# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            auth_plugin='mysql_native_password'
        )
    except Error as e:
        raise customException(e, sys)

def insert_data(data):
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = """INSERT INTO PlaceHolders 
                 (Name, Age, Gender, Phone_number, Email, Address, Nationality, Organizations, Languages_known) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            data.get("Name", ""),
            data.get("Age", ""),
            data.get("Gender", ""),
            data.get("Phone_number", ""),
            data.get("Email", ""),
            data.get("Address", ""),
            data.get("Nationality", ""),
            data.get("Organizations", ""),
            data.get("Languages_known", "")
        )
        cursor.execute(sql, values)
        db.commit()
    except Exception as e:
        raise customException(e, sys)
    finally:
        if db:
            db.close()

def fetch_data():
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""SELECT Name, Age, Gender, Phone_number, Email, Address, 
                                 Nationality, Organizations, Languages_known 
                          FROM PlaceHolders 
                          ORDER BY id DESC 
                          LIMIT 1""")
        data = cursor.fetchone()
        return data
    except Exception as e:
        raise customException(e, sys)
    finally:
        if db:
            db.close()
