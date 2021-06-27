#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2021 Jun 15 06:38:30 PM

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
#        config.base.App = "fix_lost"
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

mapCompanyManager = {}

def getCompanyManagerCount(cid):
    if cid in mapCompanyManager:
        return mapCompanyManager[cid]
    sql = """
    select company_id, count(*) from fund_fundmanager group by company_id;
    """
    db = MySQLDB(host="172.17.0.2", user="root", port=3306, pw="", db="eastmoney")
    ret = MySQLRun(db, sql)
    if ret is None:
        return 0
    for r in ret:
        if r is None:
            continue
        comid = r[0]
        count = r[1]
        mapCompanyManager[comid] = count
    if cid in mapCompanyManager:
        return mapCompanyManager[cid]
    else:
        return 0

def fill(ident):
    sql = \
    """\
    select * from fund_fundhistoricalnetworth as a left join (select fund_code, fund_type from fund_fund) b on a.fund_code = b.fund_code left join (select fund_code, manager_id from fund_fundmanagerrelationship ) c on c.fund_code = a.fund_code left join (select manager_id, company_id, working_time, total_asset_manage_amount, current_fund_best_profit from fund_fundmanager) e on e.manager_id = c.manager_id left join (select company_id, establish_date, total_manage_amount, total_fund_num, total_manager_num, tianxiang_star from fund_fundcompany ) d on e.company_id = d.company_id where a.id = {ident};\
    """.format(ident=ident)

    db = MySQLDB(host="172.17.0.2", user="root", port=3306, pw="", db="eastmoney")
    ret = MySQLRun(db, sql)
    if ret is None:
        return
    for r in ret:
        if r is None:
            break
        print (r)

        fund_code = r[1]
        cumulative_networth = r[3]
        inc_ratio = r[4]
        date = r[8]
        # 周一= 1...
        weekday = date.weekday()+1
        fund_type = r[13]
        manager_id = r[15]
        company_id = r[17]
        best_profit = r[20]
        manager_asset = r[19]
        work_time_day = r[18]
        company_st = r[22]
        company_asset = r[23]
        company_fund_count = r[24]
        company_manager_count = r[25]
        if company_manager_count == 0:
            company_manager_count = getCompanyManagerCount(company_id)
        company_tianxiang_rate = r[26]

        i_sql = """
        insert into fund_fundanalysis(`fund_code`, `inc_ratio`, `cumulative_networth`, `date`, `manager_id`, `company_id`, `best_profit`, `manager_asset`, `work_time_day`, `company_st`, `company_asset`, `company_fund_count`, `company_manager_count`, `company_tianxiang_rate`) values ("{fund_code}", {inc_ratio}, {cumulative_networth}, "{date}", "{manager_id}", "{company_id}", {best_profit}, {manager_asset}, {work_time_day}, "{company_st}", {company_asset}, {company_fund_count}, {company_manager_count}, {company_tianxiang_rate});
        """.format(fund_code=fund_code, inc_ratio=inc_ratio, cumulative_networth=cumulative_networth, date=date, manager_id=manager_id, company_id=company_id, best_profit=best_profit,manager_asset=manager_asset, work_time_day=work_time_day, company_st=company_st, company_asset=company_asset, company_fund_count=company_fund_count, company_manager_count=company_manager_count, company_tianxiang_rate=company_tianxiang_rate)
        MySQLRun(db, i_sql)
    db.commit()

def main():
    with open('infolost', 'r') as f:
        for l in f.readlines():
            l = l[:-1]
            fill(l)

if __name__ == "__main__":
    main()

