#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Nov 05 10:24:41

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import time
import datetime
from kafka import KafkaConsumer as kc

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
#if __name__ == "__main__":
#    import config.base
#    if not config.base.Configured:
#        config.base.Configured = True
#        config.base.App = "lib/kfk"
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

def KfkCons(kafka_topic="", kafka_hosts=["localhost:9092"], kafka_group="python_test"):
    cons = kc(bootstrap_servers=kafka_hosts,group_id=kafka_group)
    cons.subscribe(kafka_topic)
    return cons

def main():
    for m in KfkCons("online_topic"):
        print m
        break

if __name__ == "__main__":
    main()

