#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 16:11:24

#import os
#import sys 
#sys.path.append(os.path.abspath("../../"))
import time
import datetime

now = int(time.time())
today = int(now+8*3600)/86400*86400-8*3600
dayts = 86400
hourts = 3600
mints = 60
yesterday = today - dayts

def YMD(ts):
    return time.strftime("%Y%m%d", time.localtime(ts))

def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))

def DAY(ts):
    return time.strftime("%d", time.localtime(ts))

def TsToStr(ts,typ=0):
    """
    typ=0: ymd h:m:s
    typ=1: ymd
    typ=2: h:m:s
    """
    out = ""
    if typ == 0:
        out = time.strftime("%Y%m%d %H:%M:%S", time.localtime(ts))
    elif typ == 1:
        out = time.strftime("%Y%m%d", time.localtime(ts))
    elif typ == 2:
        out = time.strftime("%H:%M:%S", time.localtime(ts))
    return out

def YMDToTs(y, m, d):
    a = datetime.date(y,m,d)
    j = time.mktime(a.timetuple())
    return int(j)

def GetWeekday(ts):
    """
    Return day of the week, where Monday == 1 ... Sunday == 7.
    """
    d = datetime.datetime.fromtimestamp(ts)
    return d.weekday()+1

def ToStr(thing):
    if type(thing) is str:
        return thing
    elif type(thing) is unicode:
        return thing.encode("utf-8")
    elif type(thing) is int:
        return str(thing)
    elif type(thing) is float:
        return str(thing)

def ToUnicode(thing):
    if type(thing) is unicode:
        return thing
    elif type(thing) is str:
        return unicode(thing, "utf-8")
    elif type(thing) is int:
        return unicode(thing)
    elif type(thing) is float:
        return unicode(thing)

def main():
    pass

if __name__ == "__main__":
    main()

