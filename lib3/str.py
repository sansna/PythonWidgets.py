#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 16:11:24

#import os
#import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import re
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

def DeEmoji(s):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', s)


def TsToStr(ts, typ=0):
    """
    typ=0: ymd h:m:s
    typ=1: ymd
    typ=2: h:m:s
    typ=3: ymd_h:m:s
    typ=4: y-m-d h:m:s # mysql timestamp format
    """
    out = ""
    if typ == 0:
        out = time.strftime("%Y%m%d %H:%M:%S", time.localtime(ts))
    elif typ == 1:
        out = time.strftime("%Y%m%d", time.localtime(ts))
    elif typ == 2:
        out = time.strftime("%H:%M:%S", time.localtime(ts))
    elif typ == 3:
        out = time.strftime("%Y%m%d_%H:%M:%S", time.localtime(ts))
    elif typ == 4:
        out = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    return out


def YMDToTs(y, m, d):
    """
    Output ts of 00:00:00 of specified day
    """
    a = datetime.date(y, m, d)
    j = time.mktime(a.timetuple())
    return int(j)


def NextYMTs(y, m, n=1):
    """
    Input: 2020, 12
    Output: ts of 2021.01.01 0:0:0
    """
    a = YMDToTs(y, m, 1)
    if n > 0:
        while n > 0:
            n -= 1
            # no month has 32 days
            a += dayts * 32
            ym = YM(a)
            y = int(ym[:4])
            m = int(ym[4:])
            a = YMDToTs(y, m, 1)
        return a
    elif n < 0:
        while n < 0:
            n += 1
            a -= dayts
            ym = YM(a)
            y = int(ym[:4])
            m = int(ym[4:])
            a = YMDToTs(y, m, 1)
    return a


def GetDayTs(ts):
    """
    Get the timestamp of ts date's 00:00:00
    """
    ymd = YMD(ts)
    y = int(ymd[:4])
    m = int(ymd[4:6])
    d = int(ymd[6:])
    return YMDToTs(y, m, d)


def GetNextWeekdayTs(ts, day):
    """
    Get the next specified weekday's timestamp
    Input: ts, day means Monday == 1 ... Sunday == 7
    """
    wd = GetWeekday(ts)
    needts = ((day + 7 - wd) % 7)*dayts
    if needts == 0:
        needts = 7*dayts
    return GetDayTs(ts) + needts


def GetWeekday(ts):
    """
    Return day of the week, where Monday == 1 ... Sunday == 7.
    """
    d = datetime.datetime.fromtimestamp(ts)
    return d.weekday()+1


# No unicode type in python3, where str = unicode in python2
#+ bytes = str in python2.
def ToStr(thing):
    if type(thing) is str:
        return thing
    elif type(thing) is bytes:
        return thing.decode("utf-8")
    elif type(thing) is int:
        return str(thing)
    elif type(thing) is float:
        return str(thing)

def ToBytes(thing):
    if type(thing) is bytes:
        return thing
    elif type(thing) is str:
        return thing.encode("utf-8")
    else:
        return ToBytes(ToStr(thing))


def GenHtml(out):
    ret = ""
    for o in out:
        ret += "<p>"+o+"</p>"
    return ret


def main():
    pass


if __name__ == "__main__":
    main()
