#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2021 Jun 27 10:16:32 PM

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import ujson
import datetime
import requests
from lib3.decorator.safe_run import safe_run_wrap

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
#if __name__ == "__main__":
#    import config.base
#    if not config.base.Configured:
#        config.base.Configured = True
#        config.base.App = "client"
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

session = requests.session()

@safe_run_wrap
def Get(url="http://www.baidu.com", json={}, headers={}):
    """
    Usage:
    ret = Get(url, json, headers)
    type of str
    """
    resp = session.get(url, json=json, headers=headers)
    return resp.content

@safe_run_wrap
def Post(url="http://www.baidu.com", json={}, headers={}):
    """
    Usage:
    ret = Post(url, json, headers)
    type of str
    """
    resp = session.post(url, json=json, headers=headers)
    return resp.content

def main():
    a = Get()
    print(a)
    #a = Post()
    #print(a)

if __name__ == "__main__":
    main()

