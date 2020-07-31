#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Jul 31 16:15:03

#import os
#import sys 
#sys.path.append(os.path.abspath("../../"))
import time
import pandas as pd

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

def listtodict(l, names):
    dic = {}
    for i in xrange(0, len(names)):
        dic.update({names[i]:l[i]})
    return dic

def todataframe(table, names):
    l = []
    for a in table:
        l.append(listtodict(a, names))
    return pd.DataFrame(l)

def writexls(df, filename):
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, 'page1', float_format='%.5f')
    writer.save()

def WritexlsWrap(table, names, filename):
    writexls(todataframe(table, names), filename)

def main():
    names = ['mid', 'score']
    table = [
            [1, 300],
            [2, 100]
            ]
    filename = "out.xlsx"
    WritexlsWrap(table, names, filename)

if __name__ == "__main__":
    main()

