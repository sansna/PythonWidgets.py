#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2021 Jun 15 12:51:41 PM

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
#        config.base.App = "check_lost_items"
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

def main(start, stop):
    sql = \
    """\
    select * from fund_fundhistoricalnetworth where id >{start} and id <= {stop};\
    """.format(start=start, stop=stop)

    db = MySQLDB(host="172.17.0.2", user="root", port=3306, pw="", db="eastmoney")
    ret = MySQLRun(db, sql)
    if ret is None:
        return
    for r in ret:
        if r is None:
            break
        #print (r)

        ident = r[0]
        fund_code = r[1]
        #cumulative_networth = r[3]
        #inc_ratio = r[4]
        date = r[8]
        check_sql = """
        select count(*) from fund_fundanalysis where fund_code = "{fund_code}" and `date` = "{date}"
        """.format(fund_code=fund_code, date=date)
        val = MySQLRun(db, check_sql)
        if val is None:
            return
        for v in val:
            if v is None:
                continue
            if v[0] != 1:
                print(ident)

if __name__ == "__main__":
    total_offset=9646265
    step = 10000
    for i in range(0, total_offset, step):
        main(i, i+step)

