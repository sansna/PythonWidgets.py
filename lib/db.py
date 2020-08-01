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

def DB(host, user, pw="", db=""):
    return mysql.connect(host=host, user=user, password=pw, database=db)

def Run(db, query):
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def main():
    db=DB(host="172.20.82.5:3306", user="live", pw="szUWa@szUAIgG2g", db="account")
    print (Run(db, "select * from account;"))

if __name__ == "__main__":
    main()

