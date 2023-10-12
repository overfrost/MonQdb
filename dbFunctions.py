#! Python 3
# Functions to connect to (or create) a db
# Functions to perform queries or actions on db

import sqlite3
from sqlite3 import Error

def create_db_connection(db_name):
    connection = None
    try:
        connection = sqlite3.connect(database=db_name)
        print("Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def dbclose(connection):
    connection.close()
    print('DB connection is closed')

def createTable(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name}(Pos, Player, Score)')
    connection.commit()
    print(f'{table_name} has been created in the db')

def list_to_table(connection, table_name, list):
    cursor = connection.cursor()
    cursor.executemany(f'INSERT INTO {table_name} VALUES (?,?,?)',list)
    connection.commit()
    #print(f'{list} is committed to the db')