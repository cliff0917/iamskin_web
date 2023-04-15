import os
import sqlite3

import globals

def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def create_db():
    db_path = globals.config["db"]

    if not os.path.exists(db_path):
        conn, cursor = connect_db(db_path)

        cmd = '''CREATE TABLE USER(
                UID CHAR(21) NOT NULL,
                NAME CHAR(50) NOT NULL
                )'''
        cursor.execute(cmd)

        cmd = '''CREATE TABLE HISTORY(
            UID CHAR(21) NOT NULL,
            SERVICE_TYPE CHAR(10) NOT NULL,
            UPLOAD_TIME CHAR(19) NOT NULL,
            FILE_NAME CHAR(100) NOT NULL,
            PREDICT_CLASS CHAR(10) NOT NULL,
            DISPLAY_OUTPUT INT NOT NULL,
            PUBLISH_TIME CHAR(19),
            RATE INT,
            COMMENT CHAR(100)
            )'''
        cursor.execute(cmd)


def add_user(data):
    conn, cursor = connect_db(globals.config["db"])
    uid = data[0]

    cmd = """SELECT * FROM USER
        WHERE UID = ?"""
    cursor.execute(cmd, (uid,))
    cnts = cursor.fetchall()
    
    # 若此 uid 沒出現過, 則將 uid, name 加入到 user table 中
    if len(cnts) == 0:
        cmd = '''INSERT INTO USER
            (UID, NAME)
            VALUES(?, ?);'''
        cursor.execute(cmd, data)
    conn.commit()
    conn.close()


# 在 predict 的同時將 data insert 到 db 中, 此時 PUBLISH_TIME, RATE, COMMENT 皆為無意義的, 要在 share 的時候更新
def add_history(data):
    conn, cursor = connect_db(globals.config["db"])
    cmd = '''INSERT INTO HISTORY
        (UID, SERVICE_TYPE, UPLOAD_TIME, FILE_NAME, PREDICT_CLASS, DISPLAY_OUTPUT, PUBLISH_TIME, RATE, COMMENT)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    cursor.execute(cmd, data)
    conn.commit()
    conn.close()


# 在 share 的時候更新 history 中的 PUBLISH_TIME, RATE, COMMENT
def update_history(display_output_img, publish_time, rate, comment, uid, service_type, upload_time):
    data = (display_output_img, publish_time, rate, comment, uid, service_type, upload_time)
    conn, cursor = connect_db(globals.config["db"])
    cmd = """Update HISTORY set DISPLAY_OUTPUT = ?, PUBLISH_TIME = ?, RATE = ?, COMMENT = ?
            where UID = ? AND SERVICE_TYPE = ? AND UPLOAD_TIME = ?"""
    cursor.execute(cmd, data)
    conn.commit()
    cursor.close()


def get_history(uid):
    conn, cursor = connect_db(globals.config["db"])
    cmd = """SELECT SERVICE_TYPE, UPLOAD_TIME, FILE_NAME, PREDICT_CLASS FROM HISTORY
        WHERE UID = ?"""
    cursor.execute(cmd, (uid,))
    data = cursor.fetchall()
    return data


def get_comments(service_type='Skin'):
    conn, cursor = connect_db(globals.config["db"])
    cmd = """SELECT USER.UID, USER.NAME, HISTORY.UPLOAD_TIME, HISTORY.FILE_NAME, HISTORY.PREDICT_CLASS,
        HISTORY.DISPLAY_OUTPUT, HISTORY.PUBLISH_TIME, HISTORY.RATE, HISTORY.COMMENT
        FROM USER INNER JOIN HISTORY ON USER.UID = HISTORY.UID
        WHERE SERVICE_TYPE = ? AND PUBLISH_TIME != ?"""
    cursor.execute(cmd, (service_type, ''))
    data = cursor.fetchall()
    return data


def get_accounts():
    conn, cursor = connect_db(globals.config["db"])
    cmd = """SELECT * FROM USER"""
    cursor.execute(cmd)
    data = cursor.fetchall()
    return data