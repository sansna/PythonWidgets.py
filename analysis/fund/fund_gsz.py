#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2021 Jun 28 12:37:24 PM

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import datetime
from lib3.web.client import Get
from lib3.adv_str import JQProcess
from lib3.str import ToStr
from lib3.db import *

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
#if __name__ == "__main__":
#    import config.base
#    if not config.base.Configured:
#        config.base.Configured = True
#        config.base.App = "fund_gsz"
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

def GetList(idx=1, psz=200):
    h = {}
    h.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"})
    h.update({"Accept": "*/*"})
    h.update({"Referer": "http://fund.eastmoney.com/"})
    h.update({"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,fr;q=0.6"})
    h.update({"Cookie": "qgqp_b_id=2feabedf02060073038f702553cf7519; intellpositionL=1527.19px; em_hq_fls=js; HAList=a-sh-600050-%u4E2D%u56FD%u8054%u901A%2Ca-sz-300104-%u4E50%u89C6%u9000; em-quote-version=topspeed; st_si=62921066623921; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; cowCookie=true; intellpositionT=455px; st_asi=delete; EMFUND0=06-27%2009%3A54%3A59@%23%24%u62DB%u5546%u62DB%u88D5%u7EAF%u503AC@%23%24002995; EMFUND1=06-27%2009%3A55%3A25@%23%24%u56FD%u5F00%u5F00%u6CF0%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408A@%23%24003762; EMFUND2=06-27%2010%3A07%3A56@%23%24%u56FD%u5BCC%u6052%u5609%u77ED%u503A%u503A%u5238C@%23%24006703; EMFUND3=06-27%2010%3A08%3A34@%23%24%u524D%u6D77%u8054%u5408%u5148%u8FDB%u5236%u9020%u6DF7%u5408A@%23%24005933; EMFUND4=06-27%2010%3A30%3A32@%23%24%u524D%u6D77%u8054%u5408%u5148%u8FDB%u5236%u9020%u6DF7%u5408C@%23%24005934; EMFUND6=06-27%2018%3A15%3A50@%23%24%u5357%u65B9%u660C%u5143%u8F6C%u503AA@%23%24006030; EMFUND8=06-27%2021%3A52%3A59@%23%24%u524D%u6D77%u8054%u5408%u56FD%u6C11%u5065%u5EB7%u6DF7%u5408A@%23%24003581; EMFUND9=06-27%2021%3A53%3A07@%23%24%u534E%u6CF0%u4FDD%u5174%u5409%u5E74%u4E30%u6DF7%u5408%u53D1%u8D77C@%23%24004375; EMFUND7=06-28%2012%3A17%3A33@%23%24%u4E2D%u878D%u4E2D%u8BC1%u7164%u70AD%u6307%u6570%28LOF%29@%23%24168204; EMFUND5=06-28 12:33:23@#$%u4E2D%u6CF0%u84DD%u6708%u77ED%u503AA@%23%24007057; st_pvi=46207900405109; st_sp=2021-05-30%2013%3A40%3A37; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=148; st_psi=20210628123546991-112200305283-9088039788"})
    h.update({"Connection": "keep-alive"})
    h.update({"DNT": "1"})
    url = "http://api.fund.eastmoney.com/FundGuZhi/GetFundGZList?type=1&sort=3&orderType=desc&canbuy=0&pageIndex={idx}&pageSize={psz}&callback=jQuery18309645016107699462_1624842724765&_=1624854956420".format(idx=idx, psz=psz)
    print(url)
    ret = Get(url, {}, h)
    return JQProcess(ToStr(ret), ".Data.list[]|.gxrq, .bzdm, .gsz, .gszzl, .PLevel, .Discount, .Rate, .feature, .FType, .sgzt, .shzt, .IsExchg", lcut="(", rcut=")")

def main():
    idx = 1
    db = MySQLDB(host="172.17.0.2", user="root", port=3306, pw="", db="eastmoney")
    step = 10000
    while True:
        val = GetList(idx, step)
        idx += 1
        if val is None:
            break

        # Process
        for item in val:
            date = item[0]
            bzdm = item[1]
            gsz = item[2]
            gszzl = item[3]
            plevel = item[4]
            discount = item[5]
            rate = item[6]
            feature = item[7]
            ftype = item[8]
            sgzt = item[9]
            shzt = item[10]
            isexchg = item[11]

            # pre-process
            if len(rate) > 0:
                rate = rate[:-1]
            if len(gszzl) > 0:
                gszzl = gszzl[:-1]
            if plevel is None:
                plevel = "NULL"
            if discount is None:
                discount = "NULL"
            if rate is None or len(rate) == 0:
                rate = "NULL"
            if gsz.find("--") != -1 or gszzl.find("--") != -1:
                gsz = "NULL"
                gszzl = "NULL"

            insert_sql = """
            insert into fund_fundestimate (fund_code, `date`, gsz, gszzl, plevel, discount, `rate`, `feature`, ftype, sgzt, shzt, is_exchg) values("{bzdm}", "{date}", {gsz}, {gszzl}, {plevel}, {discount}, {rate}, "{feature}", "{ftype}", "{sgzt}", "{shzt}", "{isexchg}");
            """.format(bzdm=bzdm, date=date, gsz=gsz, gszzl=gszzl, plevel=plevel, discount=discount, rate=rate, feature=feature, ftype=ftype, sgzt=sgzt, shzt=shzt, isexchg=isexchg)
            MySQLRun(db, insert_sql)
        db.commit()

        # End of loop
        if len(val) != step:
            break

if __name__ == "__main__":
    main()

