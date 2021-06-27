#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Nov 17 08:40:34

#import os
#import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import datetime
from nltk.tokenize.util import is_cjk
from str import ToStr
import jq
import ujson
from decorator.safe_run import safe_run_wrap

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
#if __name__ == "__main__":
#    import config.base
#    if not config.base.Configured:
#        config.base.Configured = True
#        config.base.App = "lib/adv_str"
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
def IsCJK(char):
    return is_cjk(ToStr(char))

@safe_run_wrap
def CutToNByWidth(s, N=4):
    """
    输入字符串和需要截取的宽度
    输出截取后的字符串
    """
    out = ""
    s = ToStr(s)
    for i in s:
        if IsCJK(i):
            N -= 2
        else:
            N -= 1
        if N < 0:
            return out
        out += i
        if N == 0:
            return out

@safe_run_wrap
def JQProcess(cont="", pattern="", cols=0, lcut="", rcut=""):
    """
    cont: json原始串
    RetVal: val/list/list of list
    pattern: jq 处理模式
    cols: 默认0，自己计算若指定按照指定算
    lcut: 左边切除串标记字符,没有不切除
    rcut: 右边切除串标记字符,没有不切除
    """
    if len(lcut) != 0:
        cont = cont[cont.find(lcut)+len(lcut):]
    if len(rcut) != 0:
        cont = cont[:cont.rfind(rcut)-len(rcut)+1]

    # 需要计算cols的情况
    if pattern.find(",") != -1 and cols == 0:
        cols = pattern.count(",")+1
    else:
        cols = 1

    # Get ready for jq
    # jq input needs a dict, not a str
    cont = ujson.loads(cont)
    res = jq.all(pattern, cont)
    if len(res) == 1:
        return res[0]

    ret = []
    for i in range(0, int(len(res)/cols)):
        item = []
        for j in range(0, cols):
            item.append(res[i*cols+j])
        ret.append(item)

    return ret

def main():
    #print (IsCJK("你"))
    #print (IsCJK("h"))
    #print (CutToNByWidth("zx你会老师快递费"))
    ret = JQProcess("jQuery18305647404149292776_1624801423478({\"Data\":{\"typeStr\":\"1\",\"sort\":\"3\",\"sortType\":\"desc\",\"canbuy\":\"0\",\"gzrq\":\"2021-06-24\",\"gxrq\":\"2021-06-25\",\"list\":[{\"bzdm\":\"310388\",\"ListTexch\":\"\",\"FScaleType\":\"\",\"PLevel\":101.0,\"JJGSID\":\"80045188\",\"IsExchg\":\"0\",\"Discount\":1.0,\"Rate\":\"0.15%\",\"feature\":\"211\",\"gxrq\":\"2021-06-25\",\"jjlx3\":null,\"IsListTrade\":\"0\",\"jjlx2\":null,\"shzt\":null,\"isbuy\":\"1\",\"gzrq\":\"2021-06-24\",\"gspc\":\"0.51%\",\"gsz\":\"2.2743\",\"gszzl\":\"3.14%\",\"jzzzl\":\"2.63%\",\"dwjz\":\"2.2050\",\"gbdwjz\":\"2.2630\",\"jjjcpy\":\"SWLXXFZZHH\",\"jjlx\":null,\"gszzlcolor\":\"ui-table-up\",\"jzzzlcolor\":\"ui-table-up\"},{\"bzdm\":\"168204\",\"ListTexch\":\"2\",\"FScaleType\":\"02\",\"PLevel\":111.0,\"JJGSID\":\"80341238\",\"IsExchg\":\"0\",\"FType\":\"asdf\",\"Discount\":0.0,\"Rate\":\"0.00%\",\"feature\":\"020,050,051,054\",\"gxrq\":\"2021-06-25\",\"jjlx3\":null,\"IsListTrade\":\"1\",\"jjlx2\":null,\"shzt\":null,\"isbuy\":\"1\",\"gzrq\":\"2021-06-24\",\"gspc\":\"-0.12%\",\"gsz\":\"1.2714\",\"gszzl\":\"3.12%\",\"jzzzl\":\"3.24%\",\"dwjz\":\"1.2330\",\"gbdwjz\":\"1.2730\",\"jjjcpy\":\"ZRZZMTZSLOF\",\"jjjc\":\"LOF\",\"jjlx\":null,\"gszzlcolor\":\"ui-table-up\",\"jzzzlcolor\":\"ui-table-up\"}]},\"ErrCode\":0,\"ErrMsg\":null,\"TotalCount\":11248,\"Expansion\":null,\"PageSize\":2,\"PageIndex\":2})", ".Data.list[]|.gxrq, .gsz", lcut="(", rcut=")")
    print(ret)

if __name__ == "__main__":
    main()

