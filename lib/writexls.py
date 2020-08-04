#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Jul 31 16:15:03

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import time
import pandas as pd
from lib.decorator.safe_run import safe_run_wrap
from lib.str import TsToStr, ToUnicode

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

@safe_run_wrap
def listtodict(l, names):
    dic = {}
    for i in xrange(0, len(names)):
        dic.update({names[i]:l[i]})
    return dic

@safe_run_wrap
def todataframe(table, names):
    l = []
    for a in table:
        if type(a) is list:
            pass
        elif type(a) is tuple:
            a = list(a)
        else:
            continue
        l.append(listtodict(a, names))
    data = pd.DataFrame(l)
    # ReOrder
    data = data[names]
    return data

@safe_run_wrap
def FormPage(table, names, page_name):
    """
    table: list of (list of values), representing table
    names: columns, with order, w.r.t. table order
    page_name: write to which sheet in excel
    """
    l = []
    for a in table:
        if type(a) is list:
            pass
        elif type(a) is tuple:
            a = list(a)
        else:
            continue
        l.append(listtodict(a, names))
    data = pd.DataFrame(l)
    # ReOrder
    data = data[names]
    return {"page": page_name, "data": data}

@safe_run_wrap
def writexls(df, filename):
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, 'page1', float_format='%.5f')
    writer.save()

@safe_run_wrap
def mwritexls(dfsdict, filename):
    writer = pd.ExcelWriter(filename)
    for page, df in dfsdict.items():
        df.to_excel(writer, page, float_format='%.5f')
    writer.save()

@safe_run_wrap
def WritexlsWrap(table, names, filename="%s.xlsx"%TsToStr(today, 1)):
    """
    table = []
    table.append([1,2,3])
    table.append([4,5,6])
    names = ['mid','uid','score']
    """
    writexls(todataframe(table, names), filename)

@safe_run_wrap
def WritePagesWrap(pages_info, filename="%s.xlsx"%TsToStr(today, 1)):
    """
    pages_info: generated structure list using *FormPage* return items
    filename: file to write
    """
    writer = pd.ExcelWriter(filename)
    for i in xrange(0, len(pages_info)):
        page_info = pages_info[i]
        page_name = ToUnicode(page_info["page"])
        page_data = page_info["data"]
        page_data.to_excel(writer, page_name, float_format="%.5f")
    writer.save()

def main():
    # 单页写入
    names = ['开心', 'klasdfj', '可是独家发售']
    table = [
            [1, 300, 27],
            [2, 100, 13]
            ]
    #filename = "out.xlsx"
    WritexlsWrap(table, names)

    # 多页写入,有序
    pages = []
    pages.append(FormPage(table, names, "WOW"))
    pages.append(FormPage(table, names, "那时的发送地方"))
    pages.append(FormPage(table, names, "ZZZ"))
    WritePagesWrap(pages, "pages.xlsx")

if __name__ == "__main__":
    main()

