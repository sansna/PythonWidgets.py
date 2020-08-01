#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 16:27:39

#import os
#import sys 
#sys.path.append(os.path.abspath("../../"))
import time
import mysql.connector as mysql

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

def MySQLDB(host, user, port=3306, pw="", db=""):
    return mysql.connect(host=host, port=port, user=user, password=pw, database=db)

def MySQLRun(db, query):
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def main():
    db=MySQLDB(host="172.20.82.5", user="live", pw="", db="account")
    print (MySQLRun(db, "select * from account;"))

if __name__ == "__main__":
    main()

