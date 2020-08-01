#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Aug 01 19:14:55

#import os
#import sys 
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time

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

def main():
    def func(*args):
        """
        func(1,2,3): args=(1,2,3)
        """
        # tuple
        print(type(args))
    def func1(**kwargs):
        """
        func(a=1,b=2): kwargs={a:1,b:2}
        """
        # dic
        print(type(kwargs))

if __name__ == "__main__":
    main()

