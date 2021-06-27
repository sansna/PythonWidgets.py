#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2021 Jun 27 10:15:21 AM

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import datetime
from lib3.db import *

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
#if __name__ == "__main__":
#    import config.base
#    if not config.base.Configured:
#        config.base.Configured = True
#        config.base.App = "remove_dismissed_manager_analysis"
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
    return time.strftime("%Y-%m-%d", time.localtime(ts))

def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))

def DAY(ts):
    return time.strftime("%d", time.localtime(ts))

def RunRemove():
    last_date = YMD(yesterday)
    db = MySQLDB(host="172.17.0.2", user="root", port=3306, pw="", db="eastmoney")

    sql = """
    select fund_code as f, manager_id as m, cast(`update_time` as date) as d from fund_fundmanagerrelationship where `update_time` < "{last_date}"
    """.format(last_date=last_date)

    ret = MySQLRun(db, sql)
    if ret is None:
        return
    for r in ret:
        if r is None:
            continue
        fc = r[0]
        mi = r[1]
        d = r[2]
        remove_sql = """
        delete from fund_fundanalysis where fund_code = "{fc}" and manager_id = "{mi}" and `date` > "{d}";
        """.format(fc=fc, mi=mi, d=d)
        #print (last_date,remove_sql)
        MySQLRun(db, remove_sql)
        db.commit()


def main():
    RunRemove()

if __name__ == "__main__":
    main()

