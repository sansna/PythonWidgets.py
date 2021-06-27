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


def main():
    print (IsCJK("你"))
    print (IsCJK("h"))
    print (CutToNByWidth("zx你会老师快递费"))

if __name__ == "__main__":
    main()

