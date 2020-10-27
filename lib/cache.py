#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Oct 27 17:02:13

#import os
#import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import datetime
from redis import StrictRedis
from decorator.safe_run import safe_run_wrap

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
#if __name__ == "__main__":
#    import config.base
#    if not config.base.Configured:
#        config.base.Configured = True
#        config.base.App = "lib/redis"
#        config.base.Env = config.base.ENV_PRODUCTION

now = int(time.time())
today = int(now+8*3600)/86400*86400-8*3600
dayts = 86400
hourts = 3600
mints = 60
yesterday = today - dayts
nowdate = datetime.datetime.fromtimestamp(now)
Year = nowdate.year
Month = nowdate.month
Day = nowdate.day
BeginOfCurrentMonth = datetime.date(Year, Month, 1)
BeginOfLastMonth = (BeginOfCurrentMonth - datetime.timedelta(1)).replace(day=1)
BeginOfCurrentYear = BeginOfCurrentMonth.replace(month=1)
BeginOfLastYear = (BeginOfCurrentYear - datetime.timedelta(1)).replace(month=1, day=1)
BeginOfCurrentMonth = int(time.mktime(BeginOfCurrentMonth.timetuple()))
BeginOfLastMonth = int(time.mktime(BeginOfLastMonth.timetuple()))
BeginOfCurrentYear = int(time.mktime(BeginOfCurrentYear.timetuple()))
BeginOfLastYear = int(time.mktime(BeginOfLastYear.timetuple()))

def YMD(ts):
    return time.strftime("%Y%m%d", time.localtime(ts))

def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))

def DAY(ts):
    return time.strftime("%d", time.localtime(ts))

@safe_run_wrap
def RedisRun(c, query):
    if type(c) is dict:
        cnx = c.get('cnx')
        try:
            cnx.execute_command("ping")
        except:
            cnx = GetRedisConn(c)
            c["cnx"] = cnx
    data = cnx.execute_command(query)
    return data

@safe_run_wrap
def GetRedisConn(dic):
    host = dic.get('host')
    port = int(dic.get('port', 6379))
    pw = dic.get('pw', "")
    c = StrictRedis(host=host, port=port, password=pw)
    dic.update({"cnx": c})
    return dic

def main():
    dic = {
            "host": "127.0.0.1",
            "pw": "",
            "port": 6379,
            }
    LOCALCACHE = GetRedisConn(dic)
    print RedisRun(LOCALCACHE, "set axj 1")
    print RedisRun(LOCALCACHE, "setex axj 100 1") # ttl 100s
    print RedisRun(LOCALCACHE, "ttl axj") # ttl 100s
    print RedisRun(LOCALCACHE, "del axj")
    print RedisRun(LOCALCACHE, "mset axj 2 xjb 3")
    print RedisRun(LOCALCACHE, "mget axj xjb") # returns ['2', '3'], list of str
    print RedisRun(LOCALCACHE, "del axj xjb") # returns count of items deleted, 2

if __name__ == "__main__":
    main()

