# - *- coding: utf- 8 - *-
import sqlite3
from utils.decorators import catcherError
import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@catcherError
def db_con():
    mydb = sqlite3.connect(f'database/database.sqlite')
    mydb.row_factory = dict_factory
    return mydb

@catcherError       
def create_tables():
    mydb = db_con()
    mycursor = mydb.cursor()

    mycursor.execute(""" CREATE TABLE IF NOT EXISTS watcher (
                         id INTEGER PRIMARY KEY,
                         item_id INT,
                         status BOOL,
                         price INT,
                         create_date DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """
    )


@catcherError
def add_new_item(item_id,status,price):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO watcher (item_id,status,price) VALUES (?,?,?)""", (item_id,status,price))
    mydb.commit()
    cursor.close()

@catcherError
def select_by_item_id(item_id):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM watcher WHERE item_id = ?",(item_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@catcherError
def update_watcher(item_id, attr, val):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE watcher SET {attr} = ? WHERE item_id = ?", (val,item_id))
    mydb.commit()
    cursor.close()

