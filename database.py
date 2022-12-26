import os
import sqlite3

import globals

def create_db():
    db_path = globals.config["db"]

    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        sql = '''CREATE TABLE DISCUSS(
                GOOGLE_ID CHAR(21) NOT NULL,
                NAME CHAR(50) NOT NULL,
                EMAIL CHAR(100) NOT NULL,
                LOCALE CHAR(20) NOT NULL,
                TYPE CHAR(10) NOT NULL,
                TIME CHAR(19) NOT NULL,
                RATE INT NOT NULL,
                COMMENT CHAR(100),
                IMG_PATH CHAR(100)
            )'''
        cursor.execute(sql)


def insert(types, google_id, email, locale, name, time, rate, comment, img_path):
    conn = sqlite3.connect(globals.config["db"])
    cursor = conn.cursor()
    data = (types, google_id, email, locale, name, time, rate, comment, img_path)
    insert_cmd = '''INSERT INTO DISCUSS
        (GOOGLE_ID, NAME, EMAIL, LOCALE, TYPE, TIME, RATE, COMMENT, IMG_PATH)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    cursor.execute(insert_cmd, data)
    conn.commit()
    conn.close()


def read_data(types):
    conn = sqlite3.connect(globals.config["db"])
    cursor = conn.cursor()
    cursor.execute("SELECT Name, TIME, RATE, COMMENT, IMG_PATH FROM DISCUSS WHERE TYPE=?", (types,))
    rows = cursor.fetchall()
    return rows