#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2021 Jun 11 12:55:16 PM

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import datetime
from lib3.db import *
from lib3.send import *

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
#if __name__ == "__main__":
#    import config.base
#    if not config.base.Configured:
#        config.base.Configured = True
#        config.base.App = "analysis/fund/test"
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

def YMD2(ts):
    return time.strftime("%Y-%m-%d", time.localtime(ts))

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

daily_inserted_count = 0

def run_splitted(start, stop):
    uncommitted = 0
    global daily_inserted_count
    last_date = YMD2(yesterday)
    sql = \
    """\
    select * from fund_fundhistoricalnetworth as a left join (select fund_code, fund_type from fund_fund) b on a.fund_code = b.fund_code left join (select fund_code, manager_id from fund_fundmanagerrelationship where `update_time` > "{last_date}" ) c on c.fund_code = a.fund_code left join (select manager_id, company_id, working_time, total_asset_manage_amount, current_fund_best_profit from fund_fundmanager) e on e.manager_id = c.manager_id left join (select company_id, establish_date, total_manage_amount, total_fund_num, total_manager_num, tianxiang_star from fund_fundcompany ) d on e.company_id = d.company_id where a.id >{start} and a.id <= {stop};\
    """.format(start=start, stop=stop, last_date=last_date)



    # detailed info
    inc_cnts = {}
    dec_cnts = {}

    db = MySQLDB(host="172.17.0.2", user="root", port=3306, pw="", db="eastmoney")
    ret = MySQLRun(db, sql)
    if ret is None:
        return
    for r in ret:
        if r is None:
            break
        #print (r)

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

        l = [
                fund_code,
                inc_ratio,
                cumulative_networth,
                date,
                weekday,
                manager_id,
                company_id,
                best_profit,
                manager_asset,
                work_time_day,
                company_st,
                company_asset,
                company_fund_count,
                company_manager_count,
                company_tianxiang_rate,
                ]
        #print(l)

        i_sql = """
        insert into fund_fundanalysis(`fund_code`, `inc_ratio`, `cumulative_networth`, `date`, `manager_id`, `company_id`, `best_profit`, `manager_asset`, `work_time_day`, `company_st`, `company_asset`, `company_fund_count`, `company_manager_count`, `company_tianxiang_rate`) values ("{fund_code}", {inc_ratio}, {cumulative_networth}, "{date}", "{manager_id}", "{company_id}", {best_profit}, {manager_asset}, {work_time_day}, "{company_st}", {company_asset}, {company_fund_count}, {company_manager_count}, {company_tianxiang_rate});
        """.format(fund_code=fund_code, inc_ratio=inc_ratio, cumulative_networth=cumulative_networth, date=date, manager_id=manager_id, company_id=company_id, best_profit=best_profit,manager_asset=manager_asset, work_time_day=work_time_day, company_st=company_st, company_asset=company_asset, company_fund_count=company_fund_count, company_manager_count=company_manager_count, company_tianxiang_rate=company_tianxiang_rate)
        #print(i_sql)

        MySQLRun(db, i_sql)
        daily_inserted_count += 1
        uncommitted += 1
        if uncommitted >= 200:
            db.commit()
            uncommitted = 0
    db.commit()

    #    if inc_ratio < 0:
    #        if weekday not in dec_cnts:
    #            dec_cnts[weekday] = 1
    #        else:
    #            dec_cnts[weekday] += 1
    #    elif inc_ratio > 0:
    #        if weekday not in inc_cnts:
    #            inc_cnts[weekday] = 1
    #        else:
    #            inc_cnts[weekday] += 1
    #    #print (fund_code, inc_ratio, date.weekday())

    #for i in range(1,7):
    #    print(i,"ratio", inc_cnts[i]/dec_cnts[i])
    #print (inc_cnts, dec_cnts)

def main():
    #total_offset=9645779
    #step = 10000
    last_offset = 0 # read from file
    with open('last_offset', 'r') as f:
        last_offset = int(f.readline())
        print("lastoffset: ", last_offset)

    cur_offset = 0 # query from db
    sql_query_cur_offset = """
    select count(*) from fund_fundhistoricalnetworth;
    """
    db = MySQLDB(host="172.17.0.2", user="root", port=3306, pw="", db="eastmoney")
    ret = MySQLRun(db, sql_query_cur_offset)
    if ret is None:
        return
    for r in ret:
        if r is None:
            continue
        cur_offset = int(r[0])

    step = 10000
    for i in range(last_offset, cur_offset, step):
        run_splitted(i, i+step)
    with open('last_offset', 'w') as f:
        f.write(str(cur_offset))


if __name__ == "__main__":
    main()

    subj = "fund_daily_analysis_insert_"+YMD2(now)
    cont = str(daily_inserted_count)
    user = InitUser("1185280650@qq.com", '', 'smtp.qq.com')
    SendAsUserCont(user, "1185280650@qq.com", subj, cont, [])

