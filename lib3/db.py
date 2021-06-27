#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 16:27:39

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import time
import mysql.connector as mysql
from lib3.decorator.safe_run import safe_run_wrap

now = int(time.time())
today = int(now+8*3600)/86400*86400-8*3600
dayts = 86400
hourts = 3600
mints = 60
yesterday = today - dayts

def YMD(ts):
    return time.strftime("%Y%m%d", time.localtime(ts))

def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))

def DAY(ts):
    return time.strftime("%d", time.localtime(ts))

@safe_run_wrap
def MySQLDB(host, user, port=3306, pw="", db=""):
    return mysql.connect(host=host, port=port, user=user, password=pw, database=db)

@safe_run_wrap
def MySQLDBv2(dic):
    host = dic.get('host')
    user = dic.get('user')
    port = dic.get('port', 3306)
    pw = dic.get('pw', "")
    db = dic.get('database', "")
    cnx = mysql.connect(host=host, port=port, user=user, password=pw, database=db)
    dic.update({"cnx": cnx})
    return dic

@safe_run_wrap
def MySQLRun(db, query):
    if type(db) is dict:
        # This mode enables reconnect while timeout
        # {cnx: conn, host: x, port: x, user: x, pw: x, database: x}
        host = db["host"]
        port = db.get("port", 3306)
        user = db["user"]
        pw = db.get('pw', "")
        database = db["database"]
        cnx = db.get("cnx", MySQLDB(host, user, port, pw, database))
        if "cnx" not in db:
            db["cnx"] = cnx
        try:
            cnx.ping(reconnect=True, attempts=3, delay=5)
        except:
            cnx = MySQLDB(host, user, port, pw, database)
            db["cnx"] = cnx
        conn = cnx
    elif type(db) is mysql.connection_cext.CMySQLConnection:
        # one time run
        conn = db
    else:
        return None
    # start run
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def main():
    # One time run scripts, a bit simple to maintain.
    db=MySQLDB(host="172.20.82.5", user="live", pw="", db="account")
    print (MySQLRun(db, "select * from account limit 1;"))

    # Using this method makes it possible to reconnect when session times out
    TDB_ACNT = {"host": "172.20.82.5", "user":"live", "pw": "", "database": "account"}
    newdb = MySQLDBv2(TDB_ACNT)
    print (MySQLRun(newdb, "select * from account limit 2;"))

if __name__ == "__main__":
    main()

